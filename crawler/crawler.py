import HTMLParser
import logging
import re
import simplejson
import urllib2
import xml.dom.minidom

from engine.data.database.itemTable import addItem
from engine.data.item import Item
from engine.data.url import extractDomain, Url, UrlParseError

from myExceptions import FileEmptyOrUnsupportedType

USER_AGENT = "PS4M Crawler (contact: admin@ps4m.com)"

# Ignore item if title contains any of thses.
REJECT_TOKENS = ["cakeday", "[fixed]", "(fixed)", "upvote", "in comments", "subreddit"]

# Anything matching these regular expressions will be removed, item will still be imported.
STRIP_OUT = ["\[\d+\s*x\s*\d+\]", 
             "\[OC\]", 
             "\(x-post\s*(from|to)?\s*[\w/]+\)",
            ]

log = logging.getLogger()
parser = HTMLParser.HTMLParser()

class webFeed:
    def __init__(self, name, url, items):
        self.name = name
        self.url = url
        self.items = items   # list of (title<str>, url<Url>) pairs


def __cleanString__(str):
    STRIP_CHARS = "\n\r\t "
    result = parser.unescape(str)
    result = re.sub('<[^>]*>', '', result)  # remove all html tags
    return result.lstrip(STRIP_CHARS).rstrip(STRIP_CHARS)


def __cleanTitle__(title):
    result = title
    for r in STRIP_OUT:
        m = re.search(r, result)
        if(m is not None):
            result = result[:m.start()] + result[m.end():]
    return __cleanString__(result)


def __rejectItem__(title):
    for i in REJECT_TOKENS:
        if(i in title):
            return True
    return False


def __stringContainsMetaChar__(str):
    return re.search("\n|\t|\r", str)


def atomFactory(dom, url):
    log.debug("Creating atom web feed")

    def findBestLink(possibleLinks):
        log.debug("Num possible links: %d" % len(possibleLinks))
        link = None
        for l in possibleLinks:
            relValue = l.getAttribute("rel")
            if(relValue == "alternate"):
                link = l
                break
        if(link is None and len(possibleLinks) > 0):
            link = possibleLinks[0]
        return link.attributes['href'].nodeValue

    entryXml = dom.getElementsByTagName("entry")
    log.debug("Num entries: %d" % len(entryXml))
    items = []
    for i in entryXml:
        possibleLinks = i.getElementsByTagName("link")
        link = findBestLink(possibleLinks)

        title = i.getElementsByTagName("title")[0].firstChild.data
        if((link is None) or (title is None)):
            log.debug("Blank link or title")
            continue

        items.append((title, link))

    titleNode = dom.getElementsByTagName("title")[0]
    feedTitle = titleNode.firstChild.data

    return webFeed(feedTitle, url, items)


def crawl(input):
    webFeed = None
    if isinstance(input, Url):
        webFeed = itemFactory(input)
    else:
        webFeed = input

    log.debug("Num items: %d" % len(webFeed.items))
    for (title, url) in webFeed.items:
        url = __cleanString__(url)
        title = __cleanTitle__(title)

        if(url[0] == '/'):
            log.debug("Skipping realative url %s from %s" % (url, webFeed.url))
            continue

        if(__stringContainsMetaChar__(url) or __stringContainsMetaChar__(title)):
            log.debug("Skipping<data>%s, %s</data>" % (url, title))
            continue
            
        if(__rejectItem__(title)):
            log.debug("Rejecting item, title: %s" % (title))
            continue

        sourceUrl = webFeed.url.value

        # Try to instantiate, so we know putting in the DB is safe.
        try:
            Item(-1, url, title, sourceUrl) # use fake/stub item id
        except:
            log.warn("Bad item: %s, %s, %s" % (url, title, sourceUrl)) 
            continue

        # XXX: when the title is blank or a date, replace it with source Name?
        addItem(url, title, webFeed.url.value)


# Determine channel type, then call the appropriate function.
def itemFactory(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]
    response = opener.open(url.value)
    responseHeader = dict(response.info())

    if(url.getFileType() == '.json' and url.getDomain() == 'reddit.com'):
        return redditFactory(response, url)

    # The content-type in the header is usually useless, usually just say something like "xml".
    # Have to look at what tags are present in XML to determine RSS or ATOM
    dom = xml.dom.minidom.parseString(response.read())
    # If it has "item" tags, assume it's RSS.
    if(len(dom.getElementsByTagName("item")) > 0):
        return rssFactory(dom, url)
    # If it has "entry" tags, assume it atom.
    elif(len(dom.getElementsByTagName("entry")) > 0):
        return atomFactory(dom, url)
    # Don't know what it is or it's empty.
    else:
        raise FileEmptyOrUnsupportedType(url)


def redditFactory(urlHandle, feedUrl):
    log.debug("Creating reddit webfeed")
    NUM_ITEM_TO_SAVE = 10

    json = simplejson.load(urlHandle)
    jsonChildren = json['data']['children']

    # Get info for all of the items
    itemToScore = {}
    for child in jsonChildren:
        itemData = child['data']

        # No adult content
        if(itemData['over_18']):
            continue

        url = itemData["url"]
        title = itemData["title"]

        # No self posts. Have to check domain; can't use "is_self" value (fails on cross posts of self post).
        targetDomain = extractDomain(url).lower()
        if(targetDomain == "reddit.com"):
            continue
        
        itemToScore[(title, url)] = itemData['score']

    # Pick the best NUM_ITEM_TO_SAVE
    items = []
    sortedKeys = sorted(itemToScore, key=itemToScore.get, reverse=True)
    for i in sortedKeys[:NUM_ITEM_TO_SAVE]:
        items.append(i)

    feedTitle = jsonChildren[0]['data']['subreddit']
    return webFeed(feedTitle, feedUrl, items)


def rssFactory(dom, url):
    log.debug("rss web feed")

    # Gets the value if it's wrapped in a CDATA
    def __getNodeValue__(node):
        for i in node.childNodes:
            if i.nodeType == i.CDATA_SECTION_NODE:
                return i.data
        return node.firstChild.data

    # Get item XML
    channelNode = dom.getElementsByTagName("channel")[0]
    itemXml = channelNode.getElementsByTagName("item")
    if(len(itemXml) == 0):
        itemXml = dom.getElementsByTagName("item")
    log.debug("Num xml items: %d" % len(itemXml))

    items = []
    for i in itemXml:
        titleNode = i.getElementsByTagName("title")[0]
        # if there is not title skip the item
        if(titleNode.firstChild is None):
            log.debug("No title node")
            continue 
        title = __getNodeValue__(titleNode)

        linkNode = None
        if(len(i.getElementsByTagName("feedburner:origLink")) != 0):
            linkNode = i.getElementsByTagName("feedburner:origLink")[0]
        else:
            linkNode = i.getElementsByTagName("link")[0]
        link = linkNode.firstChild.data

        items.append((title, link))

    titleNode = channelNode.getElementsByTagName("title")[0]
    feedTitle = titleNode.firstChild.data
    return webFeed(feedTitle, url, items)
