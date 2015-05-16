import logging
from os import environ
import sys

from MySQLdb import connect, OperationalError

DATABASE_HOST = "localhost"
DATABASE_NAME = "PS4M"
DATABASE_PASSWORD = environ['DB_PASSWORD']
DATABASE_USER = "root"

__cursor__ = None
commit = None
rollback = None


def __init__():
    global __cursor__, commit, rollback
    connection = connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWORD,
                             db=DATABASE_NAME, charset='utf8')
    __cursor__ = connection.cursor()
    commit = connection.commit
    rollback = connection.rollback


__init__()
log = logging.getLogger()


def executeSql(query, paramArray = []):
    numRows = None
    try:
        numRows = __cursor__.execute(query, paramArray)
    except OperationalError as e:   # Most likely connection timed out
        log.warn("Operational Error: %s. Trying to reconnect" % (e))
        __init__()
        numRows = __cursor__.execute(query, paramArray)
    except Exception as e: 
        # Gather debug info, then reraise exception
        errorString = str(sys.exc_info()[1])
        errorString += "Query: " + query + " " + str.join(',', paramArray)
        errorString += ", Exception type: " + str(type(e))
        log.warn(errorString)
        raise

    if numRows >= 1:
        return __cursor__.fetchall()
    else:
        return []

def queryHasOneAndOnlyOneResult(query, paramArray):
    rows = executeSql(query, paramArray)
    numRows = len(rows)
    assert numRows < 2
    return numRows == 1
