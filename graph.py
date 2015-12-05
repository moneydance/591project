import networkx as nx
from makegraph import parseToGraph

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

# infile = 'makegraph/sampleoutput.txt'
# num_lines = 100
# edgelist = parseToGraph.parse(infile, num_lines)
# G = construct_graph(edgelist)
# print_edge_info(G, G.edges())
