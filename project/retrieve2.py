# Indiana Reed (ijreed)
# INFO-I427
# Assignment 5 (part 1)
# I started writing this script by copying my retrieval.py from Assignment 4 part 2. That way the search terms 
# are already handled as command line inputs, as well as converting the inverted index/document index files to
# dictionaries. Since we are only using the 'most' mode of search, I deleted the command line argument for mode, 
# along with the options for handling 'or' and 'and' queries. This means that I only use the 'most' option that 
# was previously in an if statement. The only addition that was needed was computing the TF-IDF scores of all 
# pages that were returned as hits. So, after calculating which pages are hits (those with > half of searchterms)
# I loop through the hits and calculate scores for each page. This is done by looping through the search terms, 
# calculating the normalized term frequency (ntf) and document frequency (df) for each one and then adding 
# ntf/df to the total TF-IDF score for that page. I find the ntf by referencing the # of times the word occurs 
# in the page (found in the inverted index) and then dividing it by the total # of words in the page (page length 
# found in document index). I calculate the df by finding the number of documents the search term appears in 
# (found simply by taking the length of the search term's value in the inverted index). Finally, I sort this 
# dictionary of hits and their scores in descending order of scores and then put them into a list of tuples 
# so I can print out the top 25.
# NOTE: I collaborated with Joel Park on this assignment.

import sys
import argparse
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sets import Set
import pickle

#use argparse to parse through arguments
#parser = argparse.ArgumentParser()
#variable number of search terms
#parser.add_argument('search_terms', nargs='+')
#args = parser.parse_args()

#save arguments
#search_terms = vars(args)['search_terms']

#converted to function for final project

def retrieve(search_terms):
    #stop and stem search terms
    stemmer = PorterStemmer()
    search_terms = [term for term in search_terms if term not in stopwords.words('english')]
    search_terms = [stemmer.stem(term) for term in search_terms]

    print search_terms

    invindex = {}
    docs = {}

    #read inverted index and put into dictionary (items in file separated by tabs)
    invindex_data = open('invindex.dat', 'r')
    lines = invindex_data.read().split('\n')
    invindex_data.close()
    for line in lines:
        line = line.split('\t')
        invindex[line[0]] = []
        i = 1
        while i < len(line)-2:
            invindex[line[0]] += [line[i:i+2]]
            i += 2
    
    #invindex = pickle.load(open('invindex','rb'))

    #read document index and put into dictionary (items in file separated by tabs)
    docs_data = open('docs.dat', 'r')
    lines = docs_data.read().split('\n')
    docs_data.close()
    for line in lines:
        line = line.split('\t')
        docs[line[0]] = line[1:4]

    #docs = pickle.load(open('docs', 'rb'))

    #set of page hits to be returned
    hits = Set([])

    #if mode is 'most', return pages that have at least half of the search terms
    #use dictionary where key is a page and value is number of hits
    n_page_hits = {}
    for term in search_terms:
        if term in invindex:
            for page in invindex[term]:
                #if page is not in dictionary, add it with value 1
                if page[0] not in n_page_hits:
                    n_page_hits[page[0]] = 1
                    #if page is already in dictionary, add 1 to its hit counter
                else:
                    n_page_hits[page[0]] += 1
    #loop through dictionary pages
    for page in n_page_hits:
        #if number of hits is greater than or equal to half the number of search terms
        if n_page_hits[page] >= (len(search_terms)/2):
            #add the page to the hits set
            hits.add(page)

    #compute TF-IDF scores for each page hit
    #store scores in dictionary (key is page, value is score)
    tfidf_scores = {}
    for page in hits:
        tfidf_score = 0
        for term in search_terms:
            if term in invindex:
                ntf = 0
                for item in invindex[term]:
                    if item[0] == page:
                        ntf = float(item[1])/float(docs[page][0]) #percentage of page's words that are the search term
                df = len(invindex[term]) #number of pages term appears in
                term_score = ntf/df
            else:
                #if term is not in the page, the term's score is 0
                term_score = 0
            #add each term's score to the total to compute tf-idf score (summation)
            tfidf_score += term_score
        #add page and score to dictionary
        tfidf_scores[page] = tfidf_score

    print tfidf_scores
    #instead of printing output, save tfidf scores using pickle
    pickle.dump(tfidf_scores, open('TFIDF', 'w'))

    #sort dictionary by score in descending order and save to list of tuples
    #hits_and_scores = sorted(tfidf_scores.items(), key=lambda x:x[1], reverse = True)

    #print output
    #print "Hits:"
    #i = 1
    #for item in hits_and_scores:
        #if i > 25:
            #break
        #print str(i) + "."
        #print docs[item[0]][2]
        #print docs[item[0]][1]
        #print "TF-IDF Score:", item[1]
        #i += 1
    #print "\n", len(docs), "documents searched"
    #print len(hits), "hits found"
