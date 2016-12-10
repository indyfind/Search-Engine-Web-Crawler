# Indiana Reed (ijreed)
#INFO-I427 Final Project - PageRank

import os
import sys
import numpy
import unittest
import pickle

# Unit Testing
class TestMethods(unittest.TestCase):
    def test_pagerank1(self):
        webgraph = {}
        webgraph["A"] = set(["D", "E"])
        webgraph["B"] = set(["C", "F"])
        webgraph["C"] = set(["E"])
        webgraph["D"] = set(["A","C"])
        webgraph["E"] = set(["A", "B", "C", "D", "F"])
        webgraph["F"] = set(["B","D"])
        pr = pagerank(webgraph)
        self.assertEqual(pr['A'], 0.14337797231075433)
        self.assertEqual(pr['B'], 0.11745933930189098)
        self.assertEqual(pr['C'], 0.19327849817764564)
        self.assertEqual(pr['D'], 0.17833891754732553)
        self.assertEqual(pr['E'], 0.2500859333604926)
        self.assertEqual(pr['F'], 0.11745933930189095)

# Takes a dictionary with pages as keys and links as values, returns an adjacency matrix (using numpy)
# also takes list of keys in the dictionary, to make sure they are ordered the same as in pagerank
def adjacencymatrix(graph, keys):
    n = len(keys)
    answer = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if keys[j] in graph[keys[i]]:
                if len(graph[keys[i]]) == 0:#if no outlinks:
                    answer[i][j] = 0.15 #set to dampening factor
                else:
                    answer[j][i] = float(1)/float(len(graph[keys[i]]))
    return numpy.matrix(answer)

# Takes a dictionary with pages as keys and links as values
# Returns a dictionary with pages as keys and pageranks as values
def pagerank(graph): 
    answer = {}
    keys = graph.keys()
    n = len(keys)
    adj_matrix = adjacencymatrix(graph, keys)
    google_matrix = (1.0/float(n)) * numpy.matrix(numpy.ones((n,n)))
    m = (0.85 * adj_matrix) + (0.15 * google_matrix)
    v = (1.0 / n) * numpy.ones((n,1))
    while sum(abs(m * v - v)) > 0.001:
        v = (m * v)
    v = (m*v).tolist()
    for i in range(n):
        answer[keys[i]] = v[i][0]
    return answer

# Load webgraph from pickle file
web_graph = pickle.load(open('webgraph','rb'))

# Save pageranks using pickle
pickle.dump(pagerank(web_graph), open('pageranks', 'w'))

if __name__ == '__main__':
    unittest.main()
