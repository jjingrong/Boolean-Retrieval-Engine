This is the README file for A0114395E / A0111014J's submission

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

== Files included with this submission ==
postings.txt
	- The postings of a particular term on each line
	- The last line contains the universal set of postings

dictionary.txt 
	- The dictionary indexed from NLTK's Reuter's testing corpus
	- Each line contains the term, term frequency, and pointer to a position in postings.txt to retrieve its' posting list
	- The last line contains the pointer to the last line for postings.txt to retrieve the universal set of postings

index.py
	- An indexing script to index the corpus into a dictionary from the input directory, as well as output the postings index (in the form of dictionary.txt and postings.txt)

search.py
	- A script to handle boolean queries of operators 'AND', 'OR', '(', ')' and 'NOT' in uppercase.

NOTE: There may be a format differences if you use the cmp command on the file output.

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0114395E / A0111014J, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
