#Main file that runs all the parts of the search engine
import pickle
import retrieve2
import pagerank

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
        try:
            webgraph = pickle.load(open('webgraph', 'r'))
        #if webgraph is not there, return error
        except:
            print "Web has not been crawled."
            return
        pagerank.pagerank(webgraph)
        pageranks = pickle.load(open('pageranks', 'r'))

    #retrieve the page hits from inverted index
    # and calculate TFIDF scores
    retrieve2.retrieve(search_terms)
    TFIDF = pickle.load(open('TFIDF', 'r'))

    #combine pageranks and TFIDF scores
    final = {}
    for page in TFIDF:
        final[page] = TFIDF[page] + pageranks[page]
    #sort pages by highest scores
    final = sorted(final, key=final.__getitem__).reverse()
    #take the top 20 pages (just URL's)
    final = final.keys()[:20]
    return final
    
