import sys

from expert_system.parsers.ExpertParser import ExpertParser


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000)
    except:
        print('Error opening file for reading ..!!')

    parser = ExpertParser(content)

