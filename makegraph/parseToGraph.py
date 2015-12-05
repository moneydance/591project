import networkx as nx

"""
<SEP>
2013-03-17 00:03:57.019019, 74.92.185.4,92.94.173.151,X,u,r,AA
? personalities.vets.webb.bin SRV
$ webb.bin SOA redacted"

<SEP>
"""

DATA_FLAGS = ['?', '$', '!']
SEPCOUNTMAX = 2
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
        if line == "<SEP>":
            print("sep line")
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
                    self.internal = [2]
                else:
                    self.valid = False



def parse(infile, num_lines):
    edgelist = []
    with open(infile, "r") as f:
        edge = DnsEdge()
        for i in range(num_lines):
            line = f.readline()
            edge.parse_line(line)
            if edge.sepcount == SEPCOUNTMAX:
                print('this happened')
                if edge.valid:
                    edgelist += [edge]
                edge = DnsEdge()
    return edgelist


infile = 'sampleoutput.txt'
num_lines = 100
edgelist = parse(infile, num_lines)
print(edgelist)

