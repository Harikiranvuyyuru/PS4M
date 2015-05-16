from collections import defaultdict
import logging

from data.database.itemTable import getAllNonExpiredIds, getItemIdsForSource, getSourceUrlTitleAndUrl
from data.item import Item
from .sourceManager import getSourceByUrl


log = logging.getLogger()
(categoryToNonExpiredItems, allNonExpiredItems, urlToNonAggregatorId) = ({}, [], {})


def getNonExpiredItems(categoryName=None):
    if(categoryName is None):
        return allNonExpiredItems
    else:
        return categoryToNonExpiredItems[categoryName]


def getNonAggregatorItem(item):
    url = item.url
    if(url in urlToNonAggregatorId and item.source.isAggregator()):
        return getItem(urlToNonAggregatorId[url])
    return None


def getItem(itemId):
    (sourceUrl, title, url) = getSourceUrlTitleAndUrl(itemId)
    return Item(itemId, url, title, getSourceByUrl(sourceUrl))

def report():
    # Report the number of nonexpired items per category
    categoryToSize = {}
    for i in categoryToNonExpiredItems:
        categoryToSize[i] = len(categoryToNonExpiredItems[i])
    for i in sorted(categoryToSize, key=categoryToSize.__getitem__, reverse=True):
        log.info("Nonexpired items: %s = %d" % (i, categoryToSize[i]))
    
def getSourceItems(sourceId):
    return [getItem(i) for i in getItemIdsForSource(sourceId)]

def initItemManager():
    global categoryToNonExpiredItems, allNonExpiredItems, urlToNonAggregatorId
    log.info("Initializing Item Manager")

    allNonExpiredItems = [getItem(i) for i in getAllNonExpiredIds()]
    
    # Index by category
    categoryToNonExpiredItems = defaultdict(lambda : [])    
    for i in allNonExpiredItems:
        for c in i.source.categories:
            categoryToNonExpiredItems[c].append(i)

    PRIMARY_DELIMITOR = '\001'
    file = open('var/duplicateUrlToOriginalid.txt')
    for line in file:
        line.rstrip()
        (url, original_id) = line.split(PRIMARY_DELIMITOR)
        urlToNonAggregatorId[url] = original_id
    file.close()

    report()
    
