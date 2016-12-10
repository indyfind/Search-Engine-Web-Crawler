#Main file that runs all the parts of the search engine
import pickle
import retrieve2
#import pagerank

def search(search_terms):
    #make sure search_terms list is not empty
    if len(search_terms) <= 0:
        print "Please enter a search query."
        return
    #load pageranks using pickle
    try:
        pageranks = pickle.load(open('pageranks', 'r'))
    #if pageranks are not there, try to call pageranks and calculate them
    except:
        print "Error: PageRanks not found"
        return
    #retrieve the page hits from inverted index
    # and calculate TFIDF scores
    retrieve2.retrieve(search_terms)
    TFIDF = pickle.load(open('TFIDF', 'r'))
    #combine pageranks and TFIDF scores
    final = {}
    for page in TFIDF:
        final[page] = TFIDF[page] + pageranks[page]
    #sort pages by highest scores
    final = sorted(final, key=final.__getitem__)
    final.reverse()
    #take the top 20 pages (just URL's)
    final = final[:20]
    #get page titles from docs.dat
    docs = {}
    docs_data = open('docs.dat', 'r')
    lines = docs_data.read().split('\n')
    docs_data.close()
    for line in lines:
        line = line.split('\t')
        if len(line) > 3:
            docs[line[3]] = line[2]
    titles = []
    for page in final:
        titles.append(docs[page])
    return [final, titles]
    
print search(['nintendo'])
