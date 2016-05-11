#from numpy.random import shuffle
from sklearn.cross_validation import KFold

from engine.analyzers.itemCounters import getCounter
from engine.data.database.voteTable import getAllVotesByUser
from engine.data.user import User
from engine.sourceManager import initSourceManager
from engine.itemManager import initItemManager
from engine.analyzers.itemCounters import readCounters

initSourceManager()
initItemManager()
readCounters()

votes = getAllVotesByUser('Toby')

#print("num votes:", len(votes))

id_to_vote_type = {}
for v in votes:
    id_to_vote_type[v.item.id] = v.type

# shuffle(votes)

def match_ratio(ids_to_predicted_vote_type):
    matches = 0
    for k in ids_to_predicted_vote_type.keys():
        if id_to_vote_type[k] == ids_to_predicted_vote_type[k]:
            matches += 1
    return matches / float(len(ids_to_predicted_vote_type))


for train_indexs, test_indexs in KFold(len(votes), shuffle=True):
    train_set = [votes[i] for i in train_indexs]
    test_set = [votes[i] for i in test_indexs]

    u = User('foo', train_set)

    # Score Test Set
    scores = []
    for v in test_set:
        titleScore = u.titleScorer.getScore(v.item, getCounter("title"))
        sourceScore = u.sourceScorer.getScore(v.item, getCounter("source"))
        scores.append((v.item.id, titleScore.score * sourceScore.score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    num_more_in_test_set = 0
    for v in test_set:
        if v.type == 'more':
            num_more_in_test_set += 1

    predicted_votes = ['more'] * num_more_in_test_set + ['less'] * (len(test_set) - num_more_in_test_set)
    ids = [i[0] for i in scores]
    assert(len(predicted_votes) == len(ids))
    id_to_predicted_vote = dict(zip(ids, predicted_votes))
        
    print match_ratio(id_to_predicted_vote)

    id_to_baseline_predict = {i: 'more' for i in ids}
    #print 'Baseline:', match_ratio(id_to_baseline_predict), '\n'
