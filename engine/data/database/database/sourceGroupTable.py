from databaseConnection import executeSql

GET_ALL_SOURCE_GROUPS = "select name, isViewable from sourceGroups"

def getAllSourceGroupNames():
    result = []
    rows = executeSql(GET_ALL_SOURCE_GROUPS)
    for r in rows:
        result.append(r[0])
    return result

def getViewableSourceGroups():
    result = []
    rows = executeSql(GET_ALL_SOURCE_GROUPS)
    for r in rows:
        (name, isViewable) = r
        if(isViewable):
            result.append(name)
    return result
