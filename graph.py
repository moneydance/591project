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
        print('For nodes: ' + str(n1) + ', ' + str(n2))
        edge_dict = G[n1][n2]
        for key in edge_dict:
            attributes = edge_dict[key]
            # assume we have date (string), data (list of strings)
            print("\tdate : " + attributes['date'])
            print("\tdata: ")
            for thing in attributes['data']:
                print("\t\t" + thing)

#the [20::] can walys be changed to some other amount!
def eigCent(G):
    centrality = nx.eigenvector_centrality_numpy(G)
    #print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    return centrality[-20:]


def degCent(G):
    centrality = nx.degree_centrality(G)
    #print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    return centrality[:20]
    
def hubCent(G):
    cent = nx.hits(G)
    #cent[0] =  hubs; cent[1] = authorities
    return cent[-20:]
    

def releventCenResults(dic1):            
    dic2 = {key:dic1[key] for key in dic1 if not re.search(r'\d', key)}                
    return dic2                

# infile = 'makegraph/sampleoutput.txt'
# num_lines = 100
# edgelist = parseToGraph.parse(infile, num_lines)
# G = construct_graph(edgelist)
# print_edge_info(G, G.edges())






