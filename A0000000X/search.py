import re
import nltk
import sys
import getopt

# Python script for queries

def performQueries(allQueries, dictionaryFile, postingsFile, outputFile):

    # Open queries file and do them sequentially
    # Content now stores each line
    with open(allQueries) as fileObj:
        content = fileObj.readlines()

    for eachLine in content:
        # Do each query


# TODO - Skip pointers

# Helper methods, merge/union etc
# TODO - merge for AND
def merge(list1, list2):
    resultList = []


    return []


# union for OR
def union(list1, list2):
    resultList = []
    for eachDocID in list1:
        if eachDocID not in resultList:
            resultList.append(eachDocID)
    for eachDocID in list2:
        if eachDocID not in resultList:
            resultList.append(eachDocID)

    return resultList


def usage():
    print "usage: " + sys.argv[0] + "-d output-dictionary -p output-posting -q input-queries -o output-results"

input_file_q = input_file_p = input_file_d = output_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        input_file_q = a
    elif o == '-d':
        input_file_d = a
    elif o == '-p':
        input_file_p = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_q == None or input_file_d == None or input_file_p == None or output_file == None:
    usage()
    sys.exit(2)

performQueries(input_file_q, input_file_d, input_file_p, output_file)