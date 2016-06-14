import logging
import os
import signal
import sys

from random import shuffle
from time import time, sleep

sys.path.append("..")
from crawler import crawl
from engine.data.database.databaseConnection import commit, rollback
from engine.data.database.sourceTable import getAllSources


def getLogger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    out = logging.StreamHandler()
    out.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(out)
    return log


if(len(sys.argv) != 1):
    print("%s accepts no command line arguments" % (sys.argv[0]))
    exit(1)

log = getLogger()
domainToLastRequestedTime = {}

# If this script runs longer than 7 hours, kill it.
def max_runtime_exceeded(signum, frame):
    log.error("Max runtime exceeded. Killing.")
    sys.exit(1)
signal.signal(signal.SIGALRM, max_runtime_exceeded)
signal.alarm(7 * 60 * 60)

log.info("Getting sources data")
sources = getAllSources()
shuffle(sources)

for s in sources:
    # If we've never hits this domain before or the last time we hit it was over a second ago, hit it now, don't wait!
    targetDomain = s.url.getDomain()
    if(targetDomain in domainToLastRequestedTime and domainToLastRequestedTime[targetDomain] + 1 > time()):
        sleep(1)
    try: 
        log.info("crawling %s" % (s.url.value))
        crawl(s.url, s.lookupId)
        domainToLastRequestedTime[targetDomain] = time()
    except:
        log.warn("Could not crawl %s. Error: %s" % (s.url.value, sys.exc_info()[0]))
        rollback()
        continue
    commit()

log.info("[Done]")

# Restart service, so it reads in new data from DBs
os.system("nohup ../admin/scripts/restartStartService.sh")
