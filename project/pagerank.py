# Indiana Reed (ijreed)
#INFO-I427 Final Project - PageRank

import os
import sys
import numpy
import unittest

class TestMethods(unittest.TestCase):
    def test_pagerank1(self):
        webgraph = {}
        webgraph["A"] = set(["D", "E"])
        webgraph["B"] = set(["C", "F"])
        webgraph["C"] = set(["E"])
        webgraph["D"] = set(["A","C"])
        webgraph["E"] = set(["A", "B", "C", "D", "F"])
        webgraph["F"] = set(["B","D"])
        self.assertEqual(pagerank(webgraph)['A'], 0.14337797231075433)

webgraph = {}
webgraph["A"] = set(["D", "E"])
webgraph["B"] = set(["C", "F"])
webgraph["C"] = set(["E"])
webgraph["D"] = set(["A","C"])
webgraph["E"] = set(["A", "B", "C", "D", "F"])
webgraph["F"] = set(["B","D"])

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
    v = (1.0/float(n)) * numpy.ones((n,1))
    while sum(abs(m * v - v)) > 0.001:
        v = (m * v)
    v = m*v
    v = v.tolist()
    for i in range(n):
        answer[keys[i]] = v[i][0]
    return answer

print pagerank(webgraph)

if __name__ == '__main__':
    unittest.main()
