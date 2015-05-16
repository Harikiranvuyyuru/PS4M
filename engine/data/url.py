import os
import re
import urlparse

class UrlParseError:
    def __init__(self, errorStr):
        self.errorStr = errorStr

regExStr = "(http|https|ftp)://(?:www.)?(.*?)(/|\?|$)"
regEx = re.compile(regExStr, re.IGNORECASE)

def extractDomain(url):
    domain = None

    regExResult = regEx.match(url)
    if regExResult is None:
        raise UrlParseError("Could Not get domain: %s" % url)
    matches = regExResult.groups()
    domain = matches[len(matches) - 2]

    return domain.lower()


class Url:
    def __init__(self, url):
        self.value = url
        self.domain = extractDomain(url)

    def __eq__(self, other):
        if isinstance(other, Url):
            other = other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "<Url(%s)>" % (self.value)

    def getFileType(self):
        path = urlparse.urlparse(self.value).path
        ext = os.path.splitext(path)[1]
        return ext.lower()

    def getDomain(self):
        return self.domain
