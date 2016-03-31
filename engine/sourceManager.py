from data.database.sourceGroupAssignmentTable import getSourceIdToAssignedGroups
from data.database.sourceGroupTable import getAllSourceGroupNames
from data.database.sourceTable import getAllSources

(categoryToSourceObjects, sourceCategoryNames, sourceIdToAssignments, sourceIdToSourceObject,
 unCategorizedSource) = ({}, None, None, None, None)

def getSourceById(sourceId):
    return sourceIdToSourceObject[sourceId]

def getSourceCategoryNames():
    return sourceCategoryNames

def getSources(categoryName):
    return categoryToSourceObjects[categoryName]

def getUncategorizedSource():
    return unCategorizedSource

def _addToCategoryLookup(source):
    global categoryToSourceObjects

    for c in source.categories:
        if c in categoryToSourceObjects:
            categoryToSourceObjects[c].append(source)
        else:
            categoryToSourceObjects[c] = [source]


def __sourceToCategorys(source):
    source_id = source.lookupId
    if (source_id in sourceIdToAssignments):
        return sourceIdToAssignments[source_id]
    else: 
        return []
    
def initSourceManager():
    global sourceCategoryNames, sourceIdToAssignments, sourceIdToSourceObject, unCategorizedSource
    unCategorizedSource = []

    sourceCategoryNames = getAllSourceGroupNames()
    sourceIdToAssignments = getSourceIdToAssignedGroups()

    sourceIdToSourceObject = {}
    for s in getAllSources():
        s.categories = __sourceToCategorys(s)
        sourceIdToSourceObject[s.lookupId] = s

        if(len(s.categories) != 0):
            _addToCategoryLookup(s)
        else:
            unCategorizedSource.append(s)

