import networkx as nx
from makegraph import parseToGraph
import numpy as np
import re

def construct_graph(edges):
    G = nx.MultiGraph()
    for edge in edges:
        G.add_edge(edge.internal, edge.external, date=edge.date, data=edge.data)

    return G


def print_edge_info(G, node_pairs):
    """
    given list of node pairs, print date and data info of all edges shared between them.
    """
    for (n1, n2) in node_pairs:
        print 'For nodes {}, {}:'.format(n1,n2)
        edge_dict = G[n1][n2]
        for key in edge_dict:
            attributes = edge_dict[key]
            # assume we have date (string), data (list of strings)
            print "\tdate : {}".format(attributes['date'])
            print "\tdata: "
            for thing in attributes['data']:
                print "\t\t{}".format(thing)
        print ''


def eig_cent(G):
    centrality = nx.eigenvector_centrality_numpy(G)
    centrality = relevant_cen_results(centrality)


def deg_cent(G):
    centrality = nx.degree_centrality(G)
    return relevant_cen_results(centrality)

def hub_cent(G):
    centrality = nx.hits(G)
    centrality = relevant_cen_results(centrality)


def relevant_cen_results(dic1):
    dic2 = {key:dic1[key] for key in dic1 if not re.search(r'[a-z]', key) is None}
    return dic2


# infile = '2013-03-17'
# num_edges = 10
# edgelist = parseToGraph.parse(infile, num_edges=num_edges)
# G = construct_graph(edgelist)
# print_edge_info(G, G.edges())
# centrality = deg_cent(G)
# print centrality
