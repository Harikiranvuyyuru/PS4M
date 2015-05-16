class ScoredValue:
    def __init__(self, score, infoStr):
        self.score = score
        self.value = infoStr

    def __str__(self):
        return "%s(%f)" % (self.value, self.score)
