#!/usr/bin/python

"""
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.

  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help     display this help and exit


"""

from argparse import ArgumentParser, FileType
from statistics import LinearRegression
import string
import random, sys

class shufline:
    def __init__(self, filename, lines):
        if (filename):
            f = open(filename, 'r')
            self.lines = f.read().splitlines()
            f.close()
        else:
            self.lines = lines

    def shuffle(self):
        random.shuffle(self.lines)
        return self.lines
    
    def length(self):
        return len(self.lines)

def shuffle_impl(generator, cnt, hc, repeat, inclNew):
    while ((cnt == 0 or repeat) and (generator.length() > 0)):
        for line in generator.shuffle():
            sys.stdout.write(line + ('\n' if inclNew else ''))
            cnt += 1
            if (hc != -1 and cnt >= hc):
                repeat = False
                break
    
def throw_error(err):
    match err:
        case (["unrecognized", arg]):
            sys.stderr.write("shuf: unrecognized option '" + str(arg) + "'\n")
            sys.stderr.write("Try 'shuf.py --help' for more information.\n")
        case (["invalid", arg]):
            sys.stderr.write("shuf: invalid option '" + str(arg) + "'\n")
            sys.stderr.write("Try 'shuf.py --help' for more information.\n")
        case (["linecnt", val]):
            sys.stderr.write("shuf: invalid line count: '" + str(val) + "'\n")
        case (["iarg"]):
            sys.stderr.write("shuf: option requires an argument -- 'i'\n")
        case (["invrange", val]):
            sys.stderr.write("shuf: invalid input range: '" + str(val) + "'\n")
        case (["extraop", val]):
            sys.stderr.write("shuf: extra operand '" + str(val) + "'\n")
            sys.stderr.write("Try 'shuf.py --help' for more information.\n")
        case (["i_and_e"]):
            sys.stderr.write("shuf: cannot combine -e and -i options\n")
        case (['filenotfound', file]):
            sys.stderr.write("shuf: " + str(file) + ": No such file or directory\n")
        case _:
            sys.stderr.write("shuf: Error while running command\n")
            # sys.stderr.write(str(err))

def main():
    usage_msg = """Usage: %(prog)s [OPTION]... [FILE]
  or:  %(prog)s -e [OPTION]... [ARG]...
  or:  %(prog)s -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.
  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help        display this help and exit
"""

    parser = ArgumentParser(usage = usage_msg, add_help=False, allow_abbrev=False)
    
    parser.add_argument('File', nargs='*', default=[], help="File which to permute line")

    parser.add_argument("-r", "--repeat", action='store_true', help="output lines can be repeated")
    parser.add_argument("-e", "--echo", action='store_true', help="treat each ARG as an input line")
    parser.add_argument("-i", "--input-range", "--input", action='store', help="treat each number LO through HI as an input line")
    parser.add_argument("-n", "--head-count", "--head", action='store', help="output at most COUNT lines")
    parser.add_argument("--help", action='store_true', help="display this help text and exit")

    args, unknown  = (parser.parse_known_args(sys.argv[1:]))
    args = vars(args)

    #print(unknown)

    #Handling extra arguments
    if (len(unknown) > 0):
        for elem in unknown:
            if (len(elem) > 2 and elem[0] == '-' and elem[1] == '-'):
                throw_error(["unrecognized", unknown[0]])
                return
            elif (elem[0] == '-'):
                throw_error(["invalid", unknown[0]])
                return
            else:
                args['File'].append(elem)

    #Initializing default settings
    hc = -1
    echo = False
    rng = False
    inp = False
    file = False
    cnt = 0
    lines = []

    #print(args)

    #Parsing through arguments and manipulating settings
    for arg in args.items():
        match arg:
            case ('help', True):
                sys.stdout.write(usage_msg)
                return
            case ('head_count', val):
                if (val != None):
                    try:
                        hc = int(val)
                        if (hc < 0):
                            throw_error(["linecnt", val])
                            return
                    except:
                        throw_error(["linecnt", val])
                        return
            case ('input_range', val):
                try:
                    if (val != None):
                        if (len(val) > 0 and val[0] == '-'):
                            throw_error(["invrange", ''])
                            return
                        rng = True
                        r = val.split('-', 1)
                        if (len(r) != 2):
                            if (len(r) > 0):
                                throw_error(["invrange", val[0]])
                            else:
                                throw_error(["invrange", val])
                            return
                        
                        try:
                            small = int(r[0])
                        except:
                            throw_error(["invrange", r[0]])
                            return

                        try:
                            large = int(r[1])
                        except:
                            throw_error(["invrange", r[1]])
                            return

                        if (small > large):
                            throw_error(["invrange", val[0]])
                            return
                        else:
                            lines = [(str(i)) for i in range(small, large + 1)]
                except:
                    throw_error(["invrange", val])
                    return
            case('echo', True):
                echo = True
                if (len(args['File']) != 0):
                    lines = args['File']
            case('File', params):
                #Handling case of stdin input
                if ((len(params) == 0 or (len(params) == 1 and params[0] == '-')) and (not args['echo'] and args['input_range'] == None)):
                    inp = True
                elif (not args['echo'] and args['input_range'] == None):
                    file = True
                    if (len(params) > 1):
                        throw_error(["extraop", params[1]])
                        return

    #Error handling
    if (echo and rng):
        throw_error(["i_and_e"])
        return
    elif (rng and len(args['File']) > 0):
        throw_error(["extraop", args['File'][0]])
        return

    #Reading input if necessary
    if (inp and hc != 0):
        lines = sys.stdin.read().splitlines()

    if (file):
        try:
            generator = shufline(args['File'][0], None)
            shuffle_impl(generator, cnt, hc, args['repeat'], True)
        except:
            throw_error(['filenotfound', args['File'][0]])
            return
    else:
        generator = shufline(None, lines)
        shuffle_impl(generator, cnt, hc, args['repeat'], True)


if __name__ == "__main__":
    main()