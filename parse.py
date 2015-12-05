def parse(infile, num_lines):
    with open(infile, "r") as f:
        for i in range(num_lines):
            print(f.readline())

if __name__ == '__main__':
    infile = input('name of file: ')
    num_lines = int(input('number of lines to print: '))
    parse(infile, num_lines)
