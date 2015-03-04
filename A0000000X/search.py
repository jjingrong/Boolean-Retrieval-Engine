import re
import nltk
import sys
import getopt
import math
from collections import deque

# Python script for queries

def performQueries(allQueries, dictionaryFile, postingsFile, outputFile):
    
    # Define tuples (operator, precedence)
    opLeftBracket = ('(', 5)
    opRightBracket = (')', 5)

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

    # open output file
    toOutput =  open(outputFile, 'w')

    for eachLine in content:
        outputQ = deque()
        opStack = []

        tokens = nltk.word_tokenize(eachLine)
        # Process query into the output stack and process from there
        for eachWord in tokens:
            if eachWord != '(' and eachWord != ')' and eachWord != 'NOT' and eachWord != 'AND' and eachWord != 'OR':
                queryTerm = (eachWord, 4)
                outputQ.append(queryTerm)

            # Case: Read in parenthesis
            elif eachWord != '(' and eachWord != ')':
                while len(opStack) != 0 and (opStack[len(opStack) - 1][0] == 'AND' or opStack[len(opStack) - 1][0] == 'OR' or opStack[len(opStack) - 1][0] == 'NOT'):
                    if eachWord == opNot[0]:
                        if opNot[1] < opStack[len(opStack) - 1][1]:
                            outputQ.append(opStack.pop())
                    elif eachWord == opAnd[0]:
                        if opAnd[1] < opStack[len(opStack) - 1][1]:
                            outputQ.append(opStack.pop())
                    elif eachWord == opOr[0]:
                        if opOr[1] < opStack[len(opStack) - 1][1]:
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
                while len(opStack) > 0 and opStack[len(opStack) - 1][0] != '(':
                    if not (opStack[0]):
                        break 
                    outputQ.append(opStack.pop())
                opStack.pop()

        while len(opStack) != 0:
            outputQ.append(opStack.pop())

        ##############
        # File processing
        # Get array of lines of dictionary
        dictList = []
        freqList = []
        with open(dictionaryFile) as fileObj:
            dictContents = fileObj.readlines()
        for eachLine in dictContents:
            tokens = nltk.word_tokenize(eachLine)
            dictList.append(tokens[0])
            freqList.append(tokens[1])

        allPostings = []
        fp = open(postingsFile)
        for line in enumerate(fp):
            pass
        allPostings = line[1]

        ##############
        # Process the query
        # termStack will be a list containing posting lists
        termStack = []

        # While queue is not empty
        while len(outputQ) != 0:
            while (outputQ[0])[0] != 'NOT' and (outputQ[0])[0] != 'AND' and (outputQ[0])[0] != 'OR':
                term = outputQ.popleft()
                termPostingsList = getPostingsList(term[0], dictList, freqList, postingsFile)
                termStack.append(termPostingsList)
                #for eachPosting in termPostingsList:
                #    termStack.append(eachPosting)

            if (outputQ[0])[0] == 'NOT':
                postingsListOne = termStack.pop()
                # Do NOT(postingsListOne)

            elif (outputQ[0])[0] == 'AND':
                postingsListOne = termStack.pop()
                postingsListTwo = termStack.pop()
                termStack.append(merge(postingsListOne, postingsListTwo))

            elif (outputQ[0])[0] == 'OR':
                postingsListOne = termStack.pop()
                postingsListTwo = termStack.pop()
                termStack.append(union(postingsListOne, postingsListTwo))

            outputQ.popleft()

        if termStack[0] is None:
            toOutput.write('\n')
        else:
            for eachPost in termStack[0]:
                toOutput.write(str(eachPost))
                toOutput.write(' ')
            toOutput.write('\n')


# Helper methods, merge/union etc

# complement of
#def complementOf(term, dictList, postingsFile):


# Takes in 'String', returns array of postings(int)
def getPostingsList(term, dictList, freqList, postingsFile):

    postings = []

    if term in dictList:
        lineNumberOfPostings = dictList.index(term)
    else:
        return postings

    fp = open(postingsFile)
    for i, line in enumerate(fp):
        if i == lineNumberOfPostings:
            postings = nltk.word_tokenize(line)
    print(term)
    print(postings)
    return postings


# Takes in 2 arrays, and merge
def merge(list1, list2):
    resultList = []
    i = j = 0
    # to do - Skip pointers
    iSkipPointer = int(math.sqrt(len(list1)))
    jSkipPointer = int(math.sqrt(len(list2)))

    while (i < len(list1) and j < len(list2)):
        if list1[i] == list2[j]:
            resultList.append(list1[i])
            i = i + 1
            j = j + 1
        elif int(list1[i]) < int(list2[j]):
            if ( (int(i+iSkipPointer) < len(list1)) and ( int(list1[int(i+iSkipPointer)]) < int(list2[j]))):
                i = i + iSkipPointer
            else:
                i = i+1
        else: # list1 > list2
            if ( (int(j+jSkipPointer) < len(list2)) and (int(list2[int(j+jSkipPointer)]) < int(list1[i]))):
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
    return sorted(resultList)


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