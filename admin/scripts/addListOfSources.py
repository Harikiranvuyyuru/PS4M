from collections import defaultdict
import re
import sys
import time

sys.path.append('../..')
from crawler.crawler import crawl, itemFactory
from engine.data.database.databaseConnection import commit, rollback
from engine.data.database.sourceTable import addSource, sourceExists, urlToLookupId
from engine.data.database.sourceGroupAssignmentTable import addSourceGroupAssignment
#from engine.data.database.itemTable import getSourceUrlsForItemUrl
from engine.data.url import Url


def handleLine(line):
    # Parse line
    m = lineParser.match(line.rstrip())
    assert(m.lastindex == 1 or m.lastindex == 2)
    url = Url(m.group(1))
    sourceGroupName = None
    if(m.lastindex == 2):
        sourceGroupName = m.group(2)

    # Add source
    if not sourceExists(url):
        print("Adding " + url.value)
        webFeed = itemFactory(url)
        #if not hasSimilarSource(webFeed):
        addSource(url, webFeed.name)
        sourceId = urlToLookupId(url.value)

        crawl(webFeed, sourceId)

        print "https://ps4m.com/s/%d" % (sourceId)
        #else:
        #    print "NOT ADDING!"
        #    return
    else:
        print (url.value + " already exists")

    # If nessecary, assign source to group
    if(sourceGroupName is not None):
        print "\tAdding to %s" % (sourceGroupName)
        addSourceGroupAssignment(url, sourceGroupName)
    return


def usage():
    message = """%s
NAME
    addListOfSources - adds a file of source urls
SYNOPSIS
    addListOfSources SOURCE_FILE

    SOURCE_FILE -
        Contains one url per line. Also optionally, a space then a source group.
""" % sys.argv[0]
    print message

lineParser = re.compile("^(\S+)\s?(.+)?$")

# XXX: Using this is taking too much time. Try using it again when we have an index
#        in the database to make url lookup quicker.
def hasSimilarSource(webfeed):
    duplicateUrlCounter = defaultdict(lambda:0)
    for i in webfeed.items:
        for sourceUrl in getSourceUrlsForItemUrl(i[1]):
            duplicateUrlCounter[sourceUrl] += 1

    # Print a warning, if any other webfeed has more than half of this webfeed
    result = False
    for c in duplicateUrlCounter.keys():
        if (duplicateUrlCounter[c] > len(webfeed.items)/2):
            print "Possible duplicate feed. New feed %s. Old feed: %s" % (webfeed.url, c)
            result = True
    return result 


if(len(sys.argv) != 2):
    usage()
    exit(1)

sourceFilePath = sys.argv[1]
sourceFile = open(sourceFilePath, 'r')

problemLine = set()

for line in sourceFile:
    try:
        handleLine(line)
    except Exception, e:
        rollback()
        print "fail %s: %s" % (line, e)
        problemLine.add(line)
        continue

    print # Add a blank line between sources
    commit()
    time.sleep(1)

sourceFile.close()

# Report errors
if problemLine:
    print 'Could Not Add the Following Line:'
for i in problemLine:
    print i
