from analyzers.scoredValue import ScoredValue
from data.database.voteTable import getOrderedLikedIds
from itemManager import getItem

def getUnidentifiedUserPicks(NumResults, accumulator, category=None):
    ids = getOrderedLikedIds()
    dummyScore = ScoredValue(-1, "")

    for i in ids:
        curItem = getItem(i)
        if((category is not None) and (category not in curItem.source.categories)):
            continue

        accumulator.attemptAdd(curItem, dummyScore, "unidentifedUser")

        if (len(accumulator) >= NumResults):
            break

    accumulator.finalize()
    return accumulator
