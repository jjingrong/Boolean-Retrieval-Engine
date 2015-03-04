import re
import nltk
import sys
import getopt
import os
from nltk.stem.porter import *

# Python script for indexing

def indexDictAndPosting(inPath, outDictionary, outPostings):

    getList = {}
    allWords = []
    wordFreq = {}
    allFiles = []

    # NLTK porter stemmer
    porterStem = PorterStemmer()
    directory = os.listdir(inPath)
    print(directory)

    # Open directory
    for f in directory:
        #filename is each file in the directory
        print("current file: ")
        print(f)
        allFiles.append(int(f))

        # Ignore hidden files
        if not f.startswith('.'):
            # Content now stores each line
            filename = os.path.join(inPath, f)
            with open(filename) as fileObj:
                content = fileObj.readlines()

            # Iterating through each line
            for sentence in content:
                # tokens store array of words
                tokens = nltk.word_tokenize(sentence)

                for word in tokens:
                    # Stem / lower case
                    word = word.lower()
                    word = porterStem.stem(word)

                    # Check if word already exist
                    # Case 1 : Word exist
                    if word in allWords:
                        wordFreq[word] = int(wordFreq[word]) + 1
                        if int(f) not in getList[word]:
                            getList[word].append(int(f))

                    # Case 2 : Word does not exist
                    else:
                        wordFreq[word] = 1
                        # puts docID into an array, and point the 'word' as a key to it
                        getList[word] = []
                        getList[word].append(int(f))
                        # Record the word
                        allWords.append(word)

    # All words are now finished indexing on machine's data structure, time to write them into files
    # Sort by terms then docID.

    # Sort the word
    allWords.sort()

    dictionaryOutput = open(outDictionary, 'w')
    postingOutput = open(outPostings, 'w')

    for eachWord in allWords:
        # Write into dictionary file
        dictionaryOutput.write(eachWord)
        dictionaryOutput.write(' ')
        dictionaryOutput.write(str(wordFreq[eachWord]))

        # Sort docID
        getList[eachWord].sort()

        #Write into postings file
        for eachID in getList[eachWord]:
            postingOutput.write('%s ' % eachID)
        # New line to seperate word/postings

        postingOutput.write('\n')
        dictionaryOutput.write('\n')

    allFiles.sort()
    for eachFile in allFiles:
        postingOutput.write(str(eachFile))
        postingOutput.write(' ')

def usage():
    print "usage: " + sys.argv[0] + " -i path-of-file-for-indexing -d output-dictionary -p output-posting"

indexingPath = output_file_p = output_file_d = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        indexingPath = a
    elif o == '-d':
        output_file_d = a
    elif o == '-p':
        output_file_p = a
    else:
        assert False, "unhandled option"
if indexingPath == None or output_file_p == None or output_file_d == None:
    usage()
    sys.exit(2)

#LM = build_LM(input_file_b)
#test_LM(input_file_t, output_file, LM)

dictionaryFileName = output_file_d
postingFileName = output_file_p
indexDictAndPosting(indexingPath, dictionaryFileName, postingFileName)