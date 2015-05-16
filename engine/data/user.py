from .database.voteTable import getAllVotesByUser, getAllVoteIdsByUser
from engine.analyzers.bayesScorer import BayesScorer
from engine.analyzers.keyMakers import getItemUrlDomain, getItemSource, getTitleGrams


class User:
    def __init__(self, name):
        self.name = name
        self.itemIdToVoteType = {}
        self.idsVotedOn = set()
        self.sourcesWithVotes = set()

        # Get all items user has voted on.
        votes = getAllVotesByUser(self.name)
        for v in votes:
            self.itemIdToVoteType[v.item.id] = v.type
            self.idsVotedOn.add(v.item.id)
            self.sourcesWithVotes.add(v.item.source.url.value)

        #self.destinationScorer = BayesScorer(votes, getItemUrlDomain, "urlDomain")
        self.sourceScorer = BayesScorer(votes, getItemSource, "source")
        self.titleScorer = BayesScorer(votes, getTitleGrams, "title")


    def getLikedItems(self):
        result = []
        for v in getAllVotesByUser(self.name):
            if(v.type == 'more'):
                result.append(v.item)
        return result


    def getVotes(self):
        return getAllVotesByUser(self.name)

    def hasVotedOnSource(self, item):
        return (item.source.url.value in self.sourcesWithVotes)

    def hasVotedOnItem(self, item):
        return (item.id in self.idsVotedOn)

    def voteType(self, itemId):
        if itemId not in self.itemIdToVoteType:
            return None
        return self.itemIdToVoteType[itemId]

    def updateVoteIds(self):
        self.idsVotedOn = getAllVoteIdsByUser(self.name)
