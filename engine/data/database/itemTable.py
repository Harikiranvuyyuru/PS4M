import logging

from ..url import UrlParseError

from databaseConnection import executeSql, queryHasOneAndOnlyOneResult


MAX_TITLE_LENGTH = 200
MAX_URL_LENGTH = 600

ADD_ITEM = "insert into items (url, title, sourceUrl) values (%s, %s, %s)"
GET_ALL_ITEMS = "select id, url, title, sourceUrl from items"
GET_IDS_RESTRICTED_BY_TIME = "select id from items where importedTime >= (NOW() - INTERVAL 1 DAY)"
GET_ITEM = "select * from items where url = %s and title = %s and sourceUrl = %s"
GET_ITEM_BY_ID = "select sourceUrl, title, url from items where id = %s;"
GET_ITEMS_FOR_SOURCE = "select id from items where sourceUrl in (select url from sources where lookupId = %s) order by importedTime desc limit 250"
GET_SOURCE_URL_FOR_ITEM_URL = "select sourceUrl from items where url = %s"

log = logging.getLogger()

def __getMySqlLength__(str):
    SQL = "select length(%s)"
    output = executeSql(SQL, [str])
    return output[0][0]

def __turncateTitle__(title, maxLength):
    TURNCATE_TEXT = "..."

    length = __getMySqlLength__(title)
    if(length <= maxLength):
        return title
    
    while(length + len(TURNCATE_TEXT) > maxLength):
        title = title[:title.rfind(" ")] + TURNCATE_TEXT
        length = __getMySqlLength__(title)

    return title


def addItem(url, title, sourceUrl):
    if(__getMySqlLength__(url) > MAX_URL_LENGTH):
        log.warn("URL too long: %s. From %s" % (url, sourceUrl))
        return False

    title = __turncateTitle__(title, MAX_TITLE_LENGTH)

    if(not(exists(url, title, sourceUrl))):
        executeSql(ADD_ITEM, [url, title, sourceUrl])
        return True
    return False

def exists(url, title, sourceUrl):
    return queryHasOneAndOnlyOneResult(GET_ITEM, [url, title, sourceUrl])

def getAllItems():
    return executeSql(GET_ALL_ITEMS)

def getAllNonExpiredIds():
    return [i[0] for i in executeSql(GET_IDS_RESTRICTED_BY_TIME)]

def getItemIdsForSource(lookupId):
    return [i[0] for i in executeSql(GET_ITEMS_FOR_SOURCE, [lookupId])]

def getSourceUrlsForItemUrl(url):
    return [i[0] for i in executeSql(GET_SOURCE_URL_FOR_ITEM_URL, url)]

def getSourceUrlTitleAndUrl(item_id):
    return executeSql(GET_ITEM_BY_ID, item_id)[0]
