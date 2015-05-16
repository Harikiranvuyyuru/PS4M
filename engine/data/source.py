from url import Url

AGGREGATOR_DOMAIN = set(['reddit.com', 'digg.com', 'news.ycombinator.com'])

DOMAIN_HUMAN_READABLE = {'digg.com': 'Digg', 'kplu.org': 'KPLU', 
                         'kuow.org': 'KUOW', 'npr.org': 'NPR', 
                         'reddit.com': 'reddit', 'gdata.youtube.com': 'Youtube'}


class Source:
    def __init__(self, url, name, lookupId):
        self.url = Url(url)
        self.name = name
        self.lookupId = lookupId
        self.categories = []

    def getHumanReadableName(self):
        if(self.url.getDomain() in DOMAIN_HUMAN_READABLE):
            return DOMAIN_HUMAN_READABLE[self.url.getDomain()] + ' - ' + self.name
        return self.name

    def isAggregator(self):
        return (self.url.getDomain() in AGGREGATOR_DOMAIN)

    def __repr__(self):
        return "<Source(%s, %s)>" % (self.name.encode('ascii', 'ignore'), self.url)
