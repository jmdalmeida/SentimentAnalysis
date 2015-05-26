import json
from data import DataManager


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Error: Expecting file as parameter."
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        j = json.load(f)
        dm = DataManager()
        for l in j:
            dm.process(l)
        dm.analyze()
