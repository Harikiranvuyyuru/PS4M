from databaseConnection import executeSql

ADD_GROUP_ASSIGNMENT = "insert ignore into sourceGroupAssignments (lookupId, groupName) values (%s, %s)"
GET_ALL_ASSIGNMETS = "select lookupId, groupName from sourceGroupAssignments"

def addSourceGroupAssignment(lookupId, sourceGroupName):
    executeSql(ADD_GROUP_ASSIGNMENT, [lookupId, sourceGroupName])

def getSourceIdToAssignedGroups():
    result = {}
    rows = executeSql(GET_ALL_ASSIGNMETS)
    for r in rows:
        assert len(r) == 2
        (sourceId, groupName) = r
        if sourceId not in result:
            result[sourceId] = [groupName]
        else:
            result[sourceId].append(groupName)
    return result
