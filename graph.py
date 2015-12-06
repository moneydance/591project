import networkx as nx
from makegraph import parseToGraph
import numpy as np
import re
import datetime

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
    return relevant_cen_results(centrality)


def deg_cent(G):
    centrality = nx.degree_centrality(G)
    return relevant_cen_results(centrality)

def hub_cent(G):
    centrality = nx.hits(G)
    return relevant_cen_results(centrality)


def relevant_cen_results(dic1):
    dic2 = {key:dic1[key] for key in dic1 if not re.search(r'[a-z]', key) is None}
    return dic2

def sort_by_value(dic):
    """
    Returns a list of keys in dic sorted by their values, using a simple
    variant of merge sort.
    """
    keys = list(dic.keys())
    if len(dic) <= 1:
        return keys

    k = len(keys)
    left = keys[:k//2]
    right = keys[k//2:]

    left = sort_by_value({key: dic[key] for key in left})
    right = sort_by_value({key: dic[key] for key in right})
    return _merge(left, right, dic)


def _merge(left, right, dic):
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if dic[left[i]] <= dic[right[j]]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    return merged + left[i:] if i < len(left) else merged + right[j:]


def find_rare_destinations(G, num_nodes):
    centrality = deg_cent(G)
    centrality = {key: centrality[key] for key in centrality if G.degree(key) > 3.0}
    nodes = sort_by_value(centrality)[:num_nodes]
    return nodes


def find_suspicious_edges_CNAME(G):
    susp_edges = []
    for (n1,n2) in G.edges():
        edge_dict = G[n1][n2]
        for key in edge_dict:
            data = edge_dict[key]['data']
            susp = False
            count = 0
            for thing in data:
                if 'CNAME' in thing:
                    count += 1
                    if count == 2:
                        susp_edges += [(n1,n2)]
                        susp = True
                        break
            if susp: break
    return susp_edges


def interaction_trend(G, pair):
    """
    Given G and a pair of nodes, looks at timestamps of edges and
    returns average and st deviation of intervals between interactions.
    """
    n1, n2 = pair
    edge_dict = G[n1][n2]
    # need multiple exchanges for this function to work
    assert len(list(edge_dict.keys())) > 1

    dates = [edge_dict[key]['date'] for key in edge_dict]
    dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") for date in dates]
    dates = sorted(dates)
    intervals = [(dates[i+1] - dates[i]).total_seconds() for i in range(len(dates)-1)]
    print intervals
    return np.average(intervals), np.std(intervals)

# infile = '2013-03-17'
# num_edges = 100000
# edgelist = parseToGraph.parse(infile, num_edges=num_edges)
# G = construct_graph(edgelist)
# edges = find_suspicious_edges_CNAME(G)
# edges = [edge for edge in edges if G.number_of_edges(edge[0], edge[1]) > 5]
# for edge in edges:
#     print interaction_trend(G, edge)

# print_edge_info(G, edges)
# print find_rare_destinations(G, 10)
