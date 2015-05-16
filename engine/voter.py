import logging

from data.database.databaseConnection import commit
from data.database.voteTable import addVote, deleteVote, updateVoteRecord

log = logging.getLogger()

def voteOnId(userName, itemId, action, voteType):
    if(action == "vote"):
        addVote(userName, itemId, voteType)
    elif(action == "undo"):
        deleteVote(userName, itemId)
    elif(action == "toggle"):
        updateVoteRecord(userName, itemId, voteType)
    else:
        log.warn("Unrecognized vote action: %s" % (action))
    commit()
