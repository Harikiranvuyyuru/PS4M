from data.database.sourceGroupAssignmentTable import getSourceUrlToAssignedGroups
from data.database.sourceGroupTable import getAllSourceGroupNames
from data.database.sourceTable import getAllSources

(categoryToSourceObjects, sourceCategoryNames, sourceUrlToAssignments, sourceUrlToSourceObject,
 unCategorizedSource) = ({}, None, None, None, None)

def getSourceByUrl(sourceUrl):
    return sourceUrlToSourceObject[sourceUrl]

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
    global sourceCategoryNames, sourceUrlToAssignments, sourceUrlToSourceObject, unCategorizedSource
    unCategorizedSource = []

    sourceCategoryNames = getAllSourceGroupNames()
    sourceUrlToAssignments = getSourceUrlToAssignedGroups()
    categoryToSourceUrl = {}

    sourceUrlToSourceObject = {}
    for s in getAllSources():
        s.categories = __sourceUrlToCategorys__(s)
        sourceUrlToSourceObject[s.url.value] = s

        if(len(s.categories) != 0):
            _addToCategoryLookup(s)
        else:
            unCategorizedSource.append(s)

