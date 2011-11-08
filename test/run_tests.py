import os, sys

def menu(items):
    print """\
+=============================================+
|                                             |
| {title:^43} |
|                                             |
+=============================================+
|                                             |""".format(title="Available tests")

    for i in range(len(items)):
        print "| {:>3} - {:<37} |".format(i + 1 , items[i][5:].replace('_', ' '))

    print """\
|                                             |
+=============================================+"""


def add_b3_path(b3_path):
    if not os.path.isdir(b3_path):
        print "%s not found"
        sys.exit(1)
    if not os.path.isdir(os.path.join(b3_path, 'b3')):
        print "%s does not contains the b3 module"
        sys.exit(1)
    sys.path.insert(0, b3_path)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    import argparse
    parser = argparse.ArgumentParser(description="""\
Test runner helper

To run test, the b3 module has to be in your PYTHONPATH
or B3PATH environment variable
or you can specify the location of the b3 module with the --b3path option

""")
    parser.add_argument('--b3path', metavar='B3_PATH', type=str, help='the path of the b3 module')
    parser.add_argument('--test', metavar='INDEX', dest='choice', action='store', type=int, default=None, help='# of a test to run')
    args = parser.parse_args()

    # try to get an explicit location for the b3 module
    if args.b3path:
        add_b3_path(args.b3path)
    elif 'B3PATH' in os.environ:
        add_b3_path(os.environ['B3PATH'])
    elif os.path.isdir(os.path.join(script_dir, '..', '..', 'b3')):
        add_b3_path(os.path.isdir(os.path.join(script_dir, '..', '..', 'b3')))
    else:
        #print "could not find any explicit location for the b3 module. Assuming in current PYTHONPATH"
        pass

    # add parent directory and plugin directory to the python path
    sys.path.insert(0, os.path.join(script_dir, '..'))
    sys.path.insert(0, os.path.join(script_dir, '..', 'extplugins'))

    # discover available tests
    tests = []
    import glob
    for file in glob.glob(os.path.join(script_dir, 'test_*.py')):
        tests.append(os.path.basename(file)[:-3])

    # pick a test to run
    test_index = None
    if args.choice:
        test_index = args.choice - 1
        if not 0 <= test_index < len(tests):
            print "cannot find test %s" % args.choice
            menu(tests)
            sys.exit(1)
    else:
        menu(tests)
        choice = None
        while choice is None:
            try:
                choice = int(raw_input(">"))
            except ValueError:
                print "bad choice"
                sys.exit(0)
        test_index = choice - 1
        if not 0 <= test_index < len(tests):
            print "cannot find test %s" % choice
            sys.exit(0)

    module_name = tests[test_index]

    # load the b3 module
    try:
        import b3
    except ImportError:
        print "Failed to import the b3 module\n"
        parser.print_usage()
        sys.exit(1)

    # load the test module to run
    module = __import__(module_name)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass