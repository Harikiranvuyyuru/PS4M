import cPickle
import os
from shutil import copyfile

from engine.analyzers.keyMakers import getNGrams
from engine.analyzers.counter import Counter, TextCounter

DELIMITOR = '\001'
WORK_DIR = './var'


def getDumpFilePath(column_name):
    return "%s/%s.dump" %  (WORK_DIR, column_name)

def getCountOutputFilePath(column_name):
    return "%s/%s.count" % (WORK_DIR, column_name)

def getFinalOut(column_name):
    return "%s/%s.count" % (WORK_DIR, column_name)


def dumpItemTableColumn(column_name):
    output_path = getDumpFilePath(column_name)

    # Dump all item titles to a text file.
    if os.path.isfile(output_path):
        os.remove(output_path)

    cmd = "echo 'select %s from items;' | mysql --user=root --password=$DB_PASSWORD PS4M > %s" % (column_name, output_path)
    sys_ret = os.system(cmd)
    assert(sys_ret == 0)


def aggregateColumn(colum_name):
    cmd = "sort -rn %s | uniq -c > %s" % (getDumpFilePath(colum_name), getCountOutputFilePath(colum_name))
    sys_ret = os.system(cmd)
    assert(sys_ret == 0)

def breakTitleIntoNGrams():
    input_path = getDumpFilePath('title')
    output_path = input_path + '.temp'

    titles = open(input_path)
    out = open(output_path, 'w')

    titles.readline()  # ignore header
    for line in titles:
        line = line.rstrip()

        for ngram in getNGrams(line):
            ngram = DELIMITOR.join(ngram)
            out.write(ngram + '\n')

    titles.close()
    out.close()

    # override dump file
    copyfile(output_path, input_path)


def main():
    print "Dumping Item Sources"
    dumpItemTableColumn('sourceId')
    print "Dumping Item Titles"
    dumpItemTableColumn('title')

    print "Breaking Titles into N-Grams"
    breakTitleIntoNGrams()

    print "Aggregating Sources"
    aggregateColumn('sourceId')
    print "Aggregating Titles"
    aggregateColumn('title')

    # Convert text files to python pickle files
    titleCounter = TextCounter()
    titleCounter.deserialize('./var/title.count')
    with open('./var/title.count.pickle', 'w') as f:
        cPickle.dump(titleCounter, f)

    sourceCounter = Counter()
    sourceCounter.deserialize('./var/sourceId.count')
    with open('./var/sourceId.count.pickle', 'w') as f:
        cPickle.dump(sourceCounter, f)

main()
print "[Done]"
