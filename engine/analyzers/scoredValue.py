class ScoredValue:
    def __init__(self, score, infoStr):
        self.score = score
        self.infoStr = infoStr

    def __str__(self):
        return "%s(%f)" % (self.infoStr, self.score)
