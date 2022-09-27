import argparse
import pathlib

# TODO support all types.
#   See "Data Types in https://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html
# TODO support quoted values where commas can be used inside a value


def list_arg(s):
    return s.split(',')

def check_args(args):
    first_line_data = check_csvfile(args)
    # print("Number of columns in CSV: {}\n".format(len(first_line_data)))

    for i in (args.header, args.units, args.null):
        if i is not None:
            if len(i) != len(first_line_data):
                raise ValueError("Number of columns in file does not match with the arguments")


def check_csvfile(args):
    filepath = args.csvfile
    if not filepath.exists():
        raise FileNotFoundError('File does not exist {}'.format(filepath))
    
    with open(filepath, 'r') as f:
        line = next(f)

    first_line = line.split(',')
    return first_line


def construct_line(line_data, max_lengths):
    line = "|"
    for val, m in zip(line_data, max_lengths):
        space_bef = " "*((m - len(val))//2)
        space_after = " "*(m - len(val) - len(space_bef))
        line += space_bef + val + space_after + "|"
    return line

def adjust_max_lengths(lst, max_lengths):
    for i in range(len(max_lengths)):
        max_lengths[i] = max(max_lengths[i], len(lst[i]))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts a CSV file to IPAC Table file.')
    parser.add_argument('csvfile', type=pathlib.Path, help='file to convert')
    parser.add_argument('--header',
                        action='store',
                        type=list_arg,
                        help='comma-separated column names')
    parser.add_argument('--units',
                        action='store',
                        type=list_arg,
                        help='units of the column values')
    parser.add_argument('--null',
                        action='store',
                        type=list_arg,
                        help='null value specifiers')
    
    args = parser.parse_args()
    # print(args)

    check_args(args)
    
    with open(args.csvfile, 'r') as fin:
        header = next(fin).strip().split(',') if args.header is None else args.header
        max_lengths = list(map(len, header))
        types = [None] * len(header)
        for line_num, line in enumerate(fin):
            vals = line.split(',')
            if len(vals) != len(header):
                raise ValueError('Line {} contains {} columns!'.format(
                    line_num if args.header is None else line_num + 1,
                    len(vals)))

            adjust_max_lengths(vals, max_lengths)

            for i in range(len(max_lengths)):
                was_double = types[i] == 'double'
                if types[i] != 'char':
                    try:
                        float(vals[i])
                        types[i] = 'double'
                    except Exception:
                        types[i] = 'char'
                    else:
                        if not was_double:
                            try:
                                int(vals[i])
                                types[i] = 'int'
                            except Exception:
                                pass

    adjust_max_lengths(types, max_lengths)
    

    with open(args.csvfile, 'r') as fin:
        if args.header is None:
            next(fin)

        print(construct_line(header, max_lengths))

        print(construct_line(types, max_lengths))

        if args.units is not None:
            adjust_max_lengths(args.units, max_lengths)
            print(construct_line(args.units, max_lengths))

        if args.null is not None:
            adjust_max_lengths(args.null, max_lengths)
            print(construct_line(args.null, max_lengths))

        for line in fin:
            print(construct_line(line.strip().split(','), max_lengths))


