from logging import getLogger

from data.database.userTable import getAllUserNames
from engine.data.user import User


userNameToUserObject = {}

log = getLogger()


def getUser(user_name):
    if user_name:
        user = userNameToUserObject[user_name]
        user.updateVoteIds()
        return user
    else:
        return None

def initUsers():
    global userNameToUserObject
    log.info("Caching user data")
    for cur_name in getAllUserNames():
        userNameToUserObject[cur_name] = User(cur_name)
