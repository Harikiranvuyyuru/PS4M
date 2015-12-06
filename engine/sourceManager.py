from data.database.sourceGroupAssignmentTable import getSourceUrlToAssignedGroups
from data.database.sourceGroupTable import getAllSourceGroupNames
from data.database.sourceTable import getAllSources

(categoryToSourceObjects, sourceCategoryNames, sourceUrlToAssignments, sourceIdToSourceObject,
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


def __sourceUrlToCategorys__(source):
    url = source.url.value
    if (url in sourceUrlToAssignments):
        return sourceUrlToAssignments[url]
    else: 
        return []
    
def initSourceManager():
    global sourceCategoryNames, sourceUrlToAssignments, sourceIdToSourceObject, unCategorizedSource
    unCategorizedSource = []

    sourceCategoryNames = getAllSourceGroupNames()
    sourceUrlToAssignments = getSourceUrlToAssignedGroups()
    categoryToSourceUrl = {}

    sourceIdToSourceObject = {}
    for s in getAllSources():
        s.categories = __sourceUrlToCategorys__(s)
        sourceIdToSourceObject[s.lookupId] = s

        if(len(s.categories) != 0):
            _addToCategoryLookup(s)
        else:
            unCategorizedSource.append(s)

