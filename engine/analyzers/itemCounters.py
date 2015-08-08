import cPickle
import logging

from .counter import Counter, TextCounter

counter = None
log = logging.getLogger()


def getCounter(counterName):
    return counter[counterName]

def readCounters():
    global counter
    counter = {}

    with open('./var/title.count.pickle') as f:
        counter["title"] = cPickle.load(f)

    with open('./var/sourceUrl.count.pickle') as f:
        counter["source"] = cPickle.load(f)


