from databaseConnection import executeSql
from ..vote import Vote

ADD_VOTE = "insert into votes (userName, id, type) values (%s, %s, %s)"
GET_ALL_VOTES_BY_USER = "select id, type from votes where userName = %s order by voteTime desc"
GET_ALL_VOTE_IDS_BY_USER = "select id from votes where userName = %s"
GET_ALL_MORE_VOTE_ID_ORDERED = "select id from votes where type = 'more' order by voteTime desc"
GET_ALL_VOTED_URL_BY_USER = "select i.url from votes v, items i where v.userName = %s and i.id = v.id"
DELETE_VOTE = "delete from votes where id = %s and userName = %s"
UPDATE_VOTE_TYPE = "update votes set type = %s where id = %s and userName = %s"


def addVote(userName, itemId, voteType):
    executeSql(ADD_VOTE, [userName, itemId, voteType])

def deleteVote(userName, itemId):
    executeSql(DELETE_VOTE, [itemId, userName])

def getAllVotesByUser(userName):
    rows = executeSql(GET_ALL_VOTES_BY_USER, [userName])
    result = []
    for r in rows:
        assert len(r) == 2
        (itemId, type) = r
        result.append(Vote(itemId, type))
    return result

def getAllVoteUrlsByUser(userName):
    return set([i[0] for i in executeSql(GET_ALL_VOTED_URL_BY_USER, [userName])])

def getOrderedLikedIds():
    data = executeSql(GET_ALL_MORE_VOTE_ID_ORDERED, [])
    return [x[0] for x in data]

def updateVoteRecord(userName, itemId, newType):
    executeSql(UPDATE_VOTE_TYPE, [newType, itemId, userName])
