import logging

from .counter import Counter, TextCounter

counter = None
log = logging.getLogger()


def getCounter(counterName):
    return counter[counterName]

def initializeItemCounters():
    global counter
    counter = {}

    log.debug("Reading title counter ...")
    titleCounter = TextCounter()
    titleCounter.deserialize('./var/title.count')
    counter["title"] = titleCounter

    log.debug("Building source counter ...")
    sourceCounter = Counter()
    sourceCounter.deserialize('./var/sourceUrl.count')
    counter["source"] = sourceCounter

