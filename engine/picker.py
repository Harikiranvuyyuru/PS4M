import logging

from analyzers.itemCounters import getCounter
from explorer import getTopItemsByTitle
from itemManager import getNonExpiredItems
from resultSet import DisparateResultSet
from sharer import getUnidentifiedUserPicks
from analyzers.scoredValue import ScoredValue

DEFAULT_ITEMS_PER_PAGE = 100
PAGE_NUM_TO_IGNORE_ITEM_SOURCE = 3

log = logging.getLogger()

def getPicks(user, pageNum, category=None):
    if(user is None):
        log.info("Getting unidetified user picks %s" %(category))
        result = DisparateResultSet(num_wrappers = pageNum - 1)
        return getUnidentifiedUserPicks(DEFAULT_ITEMS_PER_PAGE, result, category)

    result = None
    log.info("Picking items for %s" % (user.name))
    itemUniverse = getNonExpiredItems(category)

    if(pageNum < PAGE_NUM_TO_IGNORE_ITEM_SOURCE):
        result = DisparateResultSet(num_wrappers = pageNum - 1, filter=user.hasVotedOnItem)
        getPicksForGroup(itemUniverse, user, DEFAULT_ITEMS_PER_PAGE, result)
    
    if(result is None or len(result) < DEFAULT_ITEMS_PER_PAGE):
        if result is None:
            result = DisparateResultSet(PAGE_NUM_TO_IGNORE_ITEM_SOURCE - pageNum,
                                        filter=user.hasVotedOnItem)
        getTopItemsByTitle(itemUniverse, user, DEFAULT_ITEMS_PER_PAGE - len(result), result)

    result.finalize()
    return result


def getPicksForGroup(items, user, numRequested, resultSet):
    log.debug("Trying to pick %d results out %d items" % (numRequested, len(items)))

    # Score all possible items.
    itemsToScore = {}
    for i in items:
        # If the items has already been voted, give it a score of zero.
        if(user.hasVotedOnItem(i)):
            # XXX: aren't we filtering this out else wh
            itemsToScore[i] = ScoredValue(0, "")
            continue

        #destScore = user.destinationScorer.getScore(i, itemCounters.getCounter("urlDomain"))
        titleScore = user.titleScorer.getScore(i, getCounter("title"))
        sourceScore = user.sourceScorer.getScore(i, getCounter("source"))

        itemsToScore[i] = ScoredValue(sourceScore.score * titleScore.score, "Source =\n%s\nTitle = %s\n" % (sourceScore, titleScore))

    sortedItems = sorted(itemsToScore.iteritems(), key=lambda x: x[1].score, reverse=True)

    for i in sortedItems:
        (item, score) = i

        if(score.score <= 0):
            break

        resultSet.attemptAdd(item, score, "top")
        if(len(resultSet) >= numRequested):
            break
