from ..itemManager import getItem

class Vote:
    def __init__(self, itemId, type):
        assert(type == u'more' or type == u'less')
        self.type = type
        self.item = getItem(itemId)
