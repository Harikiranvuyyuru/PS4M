from analyzers.itemCounters import getCounter
from analyzers.scoredValue import ScoredValue

def getTopItemsByTitle(items, user, numRequested, resultSet):
    itemsToScore = {}

    for i in items:
        if(user.hasVotedOnUrl(i) or user.hasVotedOnSource(i)):
            # XXX: Maybe just drop it?
            itemsToScore[i] = ScoredValue(0, "")
            continue

        itemsToScore[i] = user.titleScorer.getScore(i, getCounter("title"))
    sortedItems = sorted(itemsToScore.iteritems(), key=lambda x: x[1].score, reverse=True)

    for i in sortedItems:
        if(len(resultSet) == numRequested):
            break

        (item, score) = i
        if(score.score <= 0):
            break

        resultSet.attemptAdd(item, score, "explorer")

