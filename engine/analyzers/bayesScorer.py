# Bayes' Theorem
# P(A|B) = P(B|A) P(A) / P(B)
# A = "like"
# B = has key value B
# P(A) = |liked| / |url|
# P(B) = |key| / |url|
# P(B|A) = |liked from B| / |liked|
# P(A|B) = ((|liked from B| / |liked|) (|liked| / |url|)) / (|key| / |url|)
#        = (|liked from B| / |url|) / (|key| / |url|) = |liked from B| / |key|


from counter import Counter
from scoredValue import ScoredValue
from itemCounters import getCounter

SMOOTHING_SCORE = 0.05  # Only used for "established" accounts

class BayesScorer:
    def __init__(self, votes, keyMaker, universeCountKey):
        self.keyMaker = keyMaker
        self.universeKeyCount = getCounter(universeCountKey)

        self.userCounters = {'more': Counter(), 'less': Counter()}

        # If this is an "established account" introduce some smoothing.
        if len(votes) > 100:
            self.init_score = SMOOTHING_SCORE
        else:
            # Don't introduce smoothing because then all items will have some score.
            # If we don't have legitimate recs to show new accounts, best to just show
            # them popular stuff.
            self.init_score = 0

        for v in votes:
            for k in keyMaker(v.item):
                if k in self.userCounters[v.type]:
                    self.userCounters[v.type][k] += 1
                else:
                    self.userCounters[v.type][k] = 1


    # XXX: shouldn't take universe count
    def getScore(self, item, universeKeyCount):
        keys = self.keyMaker(item)

        if(len(keys) < 1):
            return ScoredValue(0.0, '')
        
        debug_text = []
        score_sum = self.init_score

        for k in keys:
            cur_score = self.getKeyScore(k)
            if cur_score != 0:
                debug_text.append("[%s, %f]" % (str(k), cur_score))
                score_sum += cur_score

        debug_text = '\n\t'.join(debug_text) + '\n'

        # Normalize
        score_sum = max(0, score_sum)
        score_sum = min(1, score_sum)

        return ScoredValue(score_sum, debug_text)


    def getKeyScore(self, k):
        # XXX: quick fix. This should be refactored
        if isinstance(k, long):
            universeKey = str(k)
        else:
            universeKey = k

        if ((k in self.userCounters['more'] or k in self.userCounters['less'])
            and (universeKey in self.universeKeyCount)):
            
            moreVoteCount = 0
            if k in self.userCounters['more']:
                moreVoteCount = self.userCounters['more'][k]

            lessVoteCount = 0
            if k in self.userCounters['less']:
                lessVoteCount = self.userCounters['less'][k]

            score = float(moreVoteCount - lessVoteCount) / self.universeKeyCount[universeKey]
            assert(-1 <= score <= 1)
            return score

        return 0


    def report(self):
        sortedKeys = sorted(self.userCounters['more'].count, key=self.getKeyScore, reverse=True)

        for i in sortedKeys:
            print("%s, %s" % (i, self.getKeyScore(i)))
