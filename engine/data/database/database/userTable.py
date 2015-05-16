import hashlib
from os import environ

from databaseConnection import executeSql, queryHasOneAndOnlyOneResult

GET_ALL_USER_NAMES = 'select name from users'
GET_PASSWORD_HASH = "select passwordHash from users where name = %s"
GET_USER = "select * from users where name = %s"
INSERT_USER = "insert into users (name, passwordHash, location, createdTime) values (%s, %s, %s, NOW())"
INSERT_USER_NO_LOCATION = "insert into users (name, passwordHash, location, createdTime) values (%s, %s, NULL, NOW())"
PASSWORD_SALT = environ['USER_PASSWORD_SALT']

def __hashPassword__(passwordPlainText):
    return hashlib.sha512(PASSWORD_SALT + passwordPlainText).hexdigest()

def addUser(name, passwordPlainText, location=None):
    passwordHash = __hashPassword__(passwordPlainText)
    if(location is not None):
        executeSql(INSERT_USER, [name, passwordHash, 'NULL'])
    else:
        executeSql(INSERT_USER_NO_LOCATION, [name, passwordHash])

def authenticateUser(userName, passwordPlainText):
    return (__hashPassword__(passwordPlainText) == getSavedPasswordHash(userName))

def getAllUserNames():
    return [i[0] for i in executeSql(GET_ALL_USER_NAMES)]

def getSavedPasswordHash(userName):
    result = executeSql(GET_PASSWORD_HASH, [userName])
    if(len(result) == 1):
        return result[0][0]
    else:
        return None

def userExists(userName):
    return queryHasOneAndOnlyOneResult(GET_USER, [userName])
