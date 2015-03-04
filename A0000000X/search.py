import re
import nltk
import sys
import getopt
import math
from collections import deque

# Python script for queries

def performQueries(allQueries, dictionaryFile, postingsFile, outputFile):

    # Define operator tuples (operator, precedence)
    opLeftBracket = ('(', 4)
    opRightBracket = (')', 4)
    opNot = ('NOT', 3)
    opAnd = ('AND', 2)
    opOr = ('OR', 1)

    # Open queries file and do them sequentially
    # Content now stores each line
    with open(allQueries) as fileObj:
        content = fileObj.readlines()

    for eachLine in content:
        outputQ = deque()
        opStack = []

        # Process query into the output stack and process from there
        for eachWord in eachLine:
            if eachWord != '(' or ')' or 'NOT' or 'AND' or 'OR':
                outputQ.append(eachWord)
            elif eachWord != '(' or ')':
                while len(opStack) != 0:
                    if eachWord == opNot[0]:
                        if opNot[1] < opStack.peek()[1]:
                            outputQ.append(opStack.pop())
                    elif eachWord == opAnd[0]:
                        if opAnd[1] < opStack.peek()[1]:
                            outputQ.append(opStack.pop())
                    elif eachWord == opOr[0]:
                        if opOr[1] < opStack.peek()[1]:
                            outputQ.append(opStack.pop())

                if eachWord == opNot[0]:
                    opStack.append(opNot)
                elif eachWord == opAnd[0]:
                    opStack.append(opAnd)
                elif eachWord == opOr[0]:
                    opStack.append(opOr)

            elif eachWord == '(':
                opStack.append(opLeftBracket)
            elif eachWord == ')':
                while opStack.peek() != '(':
                    outputQ.append(opStack.pop())
                opStack.pop()

        while len(opStack) != 0:
            outputQ.append(opStack.pop())

        # Process the query

        # Do each query
        # to do - Query precedence

# Helper methods, merge/union etc
# Takes in 2 arrays, and merge
def merge(list1, list2):
    resultList = []
    i = j = 0
    # to do - Skip pointers
    iSkipPointer = math.sqrt(len(list1))
    iSkipPointer = math.floor(iSkipPointer)
    jSkipPointer = math.sqrt(len(list2))
    jSkipPointer = math.floor(jSkipPointer)

    while (i < len(list1) and j < len(list2)):
        if list1[i] == list2[j]:
            resultList.append(list1[i])
            i = i + 1
            j = j + 1
        elif list1[i] < list2[j]:
            if ( i+iSkipPointer < len(list1) and list[i+iSkipPointer] < list2[j]):
                i = i + iSkipPointer
            else:
                i = i+1
        else: # list1 > list2
            if ( j+jSkipPointer < len(list2) and list[j+jSkipPointer] < list1[i]):
                j = j + jSkipPointer
            else:
                j = j+1

    return resultList


# union for OR for 2 arrays
def union(list1, list2):
    resultList = []
    """
    Trying to make faster -> do later if got time
    -> O(2n)
    i = j = 0
    while (i < len(list1) and j < len(list2)):
        if list1[i] == list2[j]:
            resultList.append(list1[i])
            i = i + 1
            j = j + 1
        elif list1[i] < list2[j]:
            resultList.append(list1[i])
            i = i+1
        else:
            resultList.append(list2[j])
            j = j+1
    """

    # O(2n) + O(nlgn)
    for eachDocID in list1:
        if int(eachDocID) not in resultList:
            resultList.append(int(eachDocID))
    for eachDocID in list2:
        if int(eachDocID) not in resultList:
            resultList.append(int(eachDocID))

    return resultList.sort()


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