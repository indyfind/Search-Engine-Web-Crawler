#!/usr/bin/python
import cgi
import search

# Base of the html content
CONTENT = """
<html>
<title>IGNoogle</title>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<section class="webdesigntuts-workshop">
  <h1>IGNoogle</h1>
  <form action="demo.cgi" method=POST>
    <input type=text placeholder="%s" name=query>
    <button>Search</button>
  </form>
  <h2>Results</h2>
  %s
</section>
</html>

"""

def format_results(results, titles):
    final = ''
    for i in range(len(results)):
        final += '<a id="result%d" href="%s">%s</a><br>\n' % (i, results[i], titles[i])
    return final


def main():
    print "Content-Type: text/html\n\n"
    # parse form data
    form = cgi.FieldStorage()

    # get the query, if any, from the form
    if 'query' in form:
        query_str = cgi.escape(form['query'].value)
    else:
        query_str = '"empty query"'

    # TODO: process your query and get hit results
    # Result should be a list of url strings
    results,titles = search.search(query_str.split())

    # format URL strings in results into hyperlinks
    #results = None
    if results is None or len(results) == 0:
        result_str = '<h3>Empty result: No Hit</h3>'
    else:
        result_str = format_results(results, titles)

    # format your final html page
    print CONTENT % (query_str, result_str)


if __name__ == '__main__': main()
