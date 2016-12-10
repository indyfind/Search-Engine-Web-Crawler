# Indiana Reed (ijreed)
# INFO-I427
# Assignment 4
# I used two dictionaries for the inverted index and document index, with nested lists as values.
# I forced utf-8 encoding so I could write 
# to the output files by just converting things to strings. I used the Porter stemmer from nltk to stem the 
# data. I throw an error if the index file given by the user is not accessible. I chose to use BeautifulSoup 
# to strip the html and get text from the files, because it was recommended in the nltk documentation (nltk 
# had a function that has since been removed). Finally, I used the html5lib parser for beautifulsoup, 
# because I was getting an error with lxml.
# NOTE: I collaborated with Joel Park on this assignment

import sys
import nltk
import pickle
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import *



#make sure encoding is utf-8 for writing files
reload(sys)
sys.setdefaultencoding("utf-8")

#use Porter stemmer from nltk
stemmer = PorterStemmer()

folder = sys.argv[1]
index = sys.argv[2]

#try to open index file, if not found: throw error
try:
    open(folder + index, 'r')
except:
    print "File", folder+index, "does not exist. Please enter a valid index file location."
    sys.exit()

def indexer(folder, index):
    inv_index = {}
    docs = {}

    index_data = open(folder + index, 'r')
    lines = index_data.readlines()
    index_data.close()
    #loop through index
    for line in lines:
        html_doc = line.split()[0]
        url = line.split()[1]
        #open html file
        data = open(folder + html_doc, 'r')
        #use html5lib parser
        soup = BeautifulSoup(data, "html5lib")
        #close html file
        data.close()
        #save doc title
        try:
            title = soup.title.string
        except:
            title = ""
        #print title
        #strip html
        text = soup.get_text().lower()
        #tokenize text
        tokens = nltk.word_tokenize(text)
        #remove stopwords
        words = [word for word in tokens if word not in stopwords.words('english')]
        #stem words
        words = [stemmer.stem(word) for word in words]
        #save number of termsd
        n_terms = len(words)
        #update document index
        docs[html_doc] = [n_terms, title, url]
        #update inverted index
        for word in words:
            #if word not inverted index yet, add it
            if word not in inv_index:
                inv_index[word] = [[html_doc, 1]]
            #otherwise, check if the current html doc is already listed
            else:
                entered = False
                for entry in inv_index[word]:
                    if entry[0] == html_doc:
                        #if so, update the count
                        entry[1] += 1
                        entered = True
                        break
                #if not, add a tuple with current doc
                if not entered:
                    inv_index[word] += [[html_doc, 1]]
        

    #write invindex.dat file
    f = open('invindex.dat', 'w')
    for key in inv_index:
        string = str(key)
        for entry in inv_index[key]:
            for item in entry:
                string += "\t" + str(item)
        string += "\n"
        f.write(string)
    f.close()

    #pickle.dump(inv_index, open('invindex', 'w'))

    #write docs.dat file
    f = open('docs.dat', 'w')
    for key in docs:
        string = str(key)
        for entry in docs[key]:
            string += "\t" + str(entry)
        string += "\n"
        f.write(string)
    f.close()

    #pickle.dump(docs, open('docs', 'w'))

indexer(folder, index)
