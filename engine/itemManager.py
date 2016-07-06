from collections import defaultdict
import logging

from data.database.itemTable import getAllItemsForUrl, getAllNonExpiredIds, getItemIdsForSource, getSourceUrlTitleAndUrl
from data.item import Item
from .sourceManager import getSourceById


log = logging.getLogger()
(categoryToNonExpiredItems, allNonExpiredItems) = ({}, [])


def getNonExpiredItems(categoryName=None):
    if(categoryName is None):
        return allNonExpiredItems
    else:
        return categoryToNonExpiredItems[categoryName]


def getNonAggregatorItem(item, silent=False):
    if not item.source.isAggregator():
        return item
    candidates = getAllItemsForUrl(item.url.value)
    for c in candidates:
        c = getItem(c)
        if not c.source.isAggregator():
            if not silent:
                print("none agg -", item.id, '->', c.id)
            return c
    return None



def getItem(itemId):
    (sourceId, title, url) = getSourceUrlTitleAndUrl(itemId)
    return Item(itemId, url, title, getSourceById(sourceId))

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
    global categoryToNonExpiredItems, allNonExpiredItems
    log.info("Initializing Item Manager")

    allNonExpiredItems = [getItem(i) for i in getAllNonExpiredIds()]
    
    # Index by category
    categoryToNonExpiredItems = defaultdict(lambda : [])    
    for i in allNonExpiredItems:
        for c in i.source.categories:
            categoryToNonExpiredItems[c].append(i)

    report()
    
