import argparse
import sys


class Cmd:
    parser = argparse.ArgumentParser(description='ExpertSystem @ Paris 42 School - Made by @abbensid and @jterrazz')
    parser.add_argument("-m", "--mode", choices=['shell', 'interactive'], default='mode_shell', help="Interface mode")
    parser.add_argument("-g", "--graph", action='store_true', help="Displays the graph")
    parser.add_argument("-r", "--rules", action='store_true', help="Displays the rules")
    parser.add_argument("-i", "--image", action='store_true', help="Outputs the graph as an image")
    parser.add_argument("-s", "--history", action='store_true', help="Keep old states in memory")
    parser.add_argument("-v", "--verbose", action='store_true', help="Displays the steps of the resolution")

    if not hasattr(sys, '_called_from_test'):
        parser.add_argument("input", help="The file containing rules, facts and queries")
    else:
        parser.add_argument("input", nargs='?', help="The file containing rules, facts and queries")
    args = parser.parse_args()
