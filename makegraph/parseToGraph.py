import networkx as nx

"""
<SEP>
2013-03-17 00:03:57.019019, 74.92.185.4,92.94.173.151,X,u,r,AA
? personalities.vets.webb.bin SRV
$ webb.bin SOA redacted"

<SEP>
"""

DATA_FLAGS = ['?', '$', '!']
SEPCOUNTMAX = 1
RESPONSE = 'r'
ADDRESSLOOKUP = 'A'

class DnsEdge():
    def __init__(self):
        self.valid = True
        self.sepcount = 0
        self.internal = None  # ip address
        self.external = None  # domain name
        self.date = None
        self.data = []

    def parse_line(self, line):
        if line:
            if line == "<SEP>":
                self.sepcount += 1
            elif self.valid:     # If not valid then just read lines to next SEP
                starting_char = line[0]
                if starting_char in DATA_FLAGS:  # line contains Data
                    self.data += [line]
                    if starting_char == '?':
                        components = line.split()
                        if components[2] == ADDRESSLOOKUP:
                            self.external = components[1]
                        else:
                            self.valid = False
                else:
                    components = [x.strip() for x in line.split(',')]
                    if components[5] == RESPONSE:
                        self.date = components[0]
                        self.internal = components[2]
                    else:
                        self.valid = False


def parse(infile, num_lines=None, num_edges=1000):
    if num_lines:
        edgelist = []
        with open(infile, "r") as f:
            edge = DnsEdge()
            for i in range(num_lines):
                line = f.readline().rstrip()
                edge.parse_line(line)
                if edge.sepcount == SEPCOUNTMAX:
                    if edge.valid:
                        edgelist += [edge]
                    edge = DnsEdge()
        return edgelist
    else:
        edgelist = []
        edge_count = 0
        with open(infile, "r") as f:
            edge = DnsEdge()
            for line in f:
                if edge_count >= num_edges:
                    break
                line = line.rstrip()
                edge.parse_line(line)
                if edge.sepcount == SEPCOUNTMAX:
                    if edge.valid:
                        edgelist += [edge]
                        edge_count += 1
                    edge = DnsEdge()
        return edgelist
