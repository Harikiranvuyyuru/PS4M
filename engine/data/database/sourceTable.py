from databaseConnection import executeSql, queryHasOneAndOnlyOneResult
from ..source import Source

ADD_SOURCE = "insert into sources (url, name) values (%s, %s)"
GET_ALL_SOURCES = "select url, name, lookupId from sources"
GET_ID = "select lookupId from sources where url = %s"
GET_SOURCE = "select url, name from sources where url = %s"

def addSource(url, name):
    executeSql(ADD_SOURCE, [url.value, name])

def getAllSources():
    rows = executeSql(GET_ALL_SOURCES)
    result = []
    for r in rows:
        assert len(r) == 3
        (url, name, lookupId) =  r
        s = Source(url, name, lookupId)
        result.append(s)
    return result

def urlToLookupId(url):
    record = executeSql(GET_ID, [url])
    return record[0][0]

def sourceExists(url):
    return queryHasOneAndOnlyOneResult(GET_SOURCE, [url.value])
