from copy import copy

from itemManager import getNonAggregatorItem


class ResultSet:
    def __init__(self, items=None):
        self.linkTypes = set()
        self.itemToScore = {}
        self.items = []

        if items:
            for i in items:
                self.add(i)


    def __len__(self):
        return len(self.items)
        
    def add(self, item, scoreInfo=None, debugText=None):
        # Copy the item, then set its groupName.
        # One item can be associated with more than one groupName.
        item = copy(item)

        if(scoreInfo is not None and debugText is not None):
            item.debugText = "%s -\n%s" % (debugText, scoreInfo)
            self.itemToScore[item] = scoreInfo.score

        self.linkTypes.add(item.linkType)
        self.items.append(item)

    def finalize(self):
        self.items = sorted(self.items, key=lambda x: self.itemToScore[x], reverse=True)


class DisparateResultSet(ResultSet):
    MAX_PER_SOURCE = 2
    
    '''
    num_wrappers - The number of DisparateResultSets that attemptAdd before trying to add to this
        set. If any of those sets accept it, it will not be added to this set. Useful for results 
        generating items for non-front (i.e. first) page views. 
    filter - Arbitatrary function called on all item's URL. If it evaluates to true, the item is not 
        added.
    '''
    def __init__(self, num_wrappers = 0, filter = lambda x : False):
        ResultSet.__init__(self)

        if(num_wrappers > 0):
            self.wrapper = DisparateResultSet(num_wrappers-1, filter)
        else:
            self.wrapper = None
        self.filter = filter

        self.sourceCounter = {}
        self.urls = set()



    def attemptAdd(self, item, scoreInfo=None, debugText=None):
        # If this is a link from an aggregator, try to replace it with (hopefully) the original source
        if getNonAggregatorItem(item) is not None:
            item = getNonAggregatorItem(item)

        if(self.filter(item)):
            return False
        if(item.url in self.urls):
            return False
        if(self.wrapper is not None and self.wrapper.attemptAdd(item)):
            return False

        s = item.source
        
        # Update source counter
        if(s not in self.sourceCounter):
            self.sourceCounter[s] = 1
        else:
            self.sourceCounter[s] += 1
            
        if(self.sourceCounter[s] <= DisparateResultSet.MAX_PER_SOURCE):
            ResultSet.add(self, item, scoreInfo, debugText)
            self.urls.add(item.url)
            return True
        return False
