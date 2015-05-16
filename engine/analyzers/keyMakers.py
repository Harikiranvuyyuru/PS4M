import re


MAX_N_GRAM_SIZE = 3
MIN_N_GRAM_SIZE = 1
WORD_STOP_LIST_FILE = "engine/analyzers/wordStopList.txt"


stopList = set()
f = open(WORD_STOP_LIST_FILE, 'r')
for line in f:
    stopList.add(line.rstrip())
f.close()


def getItemUrlDomain(item):
    return [item.url.getDomain()]

def getItemSource(item):
    return (item.source.url.value,)   # Returns a tuple

def getTitleGrams(item):
    return getNGrams(item.title)

def getNGrams(string):
    # Tokenizes and convert to lower case
    tokens = re.findall(r'[\w\'\/]+', string)
    tokens = [i.lower() for i in tokens]

    allNgrams = []
    for n in range(MIN_N_GRAM_SIZE, MAX_N_GRAM_SIZE + 1):
        # Generate all ngrams, from title, of size n
        for j in range(0, len(tokens) - (n-1)):
            # Create curent ngram
            curGram = []
            for k in range (0, n):
                curGram.append(tokens[j+k])
            allNgrams.append(tuple(curGram))

    # Remove any tuples that contain stoplisted words
    result = []
    for curNgram in allNgrams:
        hasStopWord = False
        for token in curNgram:
            if(token in stopList):
                hasStopWord = True
                break
        if(not hasStopWord):
            result.append(curNgram)

    return result
