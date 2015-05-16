from databaseConnection import executeSql

ADD_GROUP_ASSIGNMENT = "insert ignore into sourceGroupAssignments (sourceUrl, groupName) values (%s, %s)"
GET_ALL_ASSIGNMETS = "select sourceUrl, groupName from sourceGroupAssignments"

def addSourceGroupAssignment(url, sourceGroupName):
    executeSql(ADD_GROUP_ASSIGNMENT, [url.value, sourceGroupName])

def getSourceUrlToAssignedGroups():
    result = {}
    rows = executeSql(GET_ALL_ASSIGNMETS)
    for r in rows:
        assert len(r) == 2
        (sourceUrl, groupName) = r
        if sourceUrl not in result:
            result[sourceUrl] = [groupName]
        else:
            result[sourceUrl].append(groupName)
    return result
