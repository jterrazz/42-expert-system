import argparse


class ESCmd:
    flag = argparse.ArgumentParser(description='ExpertSystem @ Paris 42 School - Made by @abbensid and @jterrazz')
    flag.add_argument("-m", "--mode", choices=['shell', 'interactive'], default='mode_shell', help="Interface mode")
    flag.add_argument("-g", "--graph", action='store_true', help="Displays the graph")
    flag.add_argument("-r", "--rules", action='store_true', help="Displays the rules")
    flag.add_argument("-i", "--image", action='store_true', help="Outputs the graph as an image")
    flag.add_argument("-s", "--history", action='store_true', help="Keep old states in memory")
    flag.add_argument("-v", "--verbose", action='store_true', help="Displays the steps of the resolution")
    flag.add_argument("input", help="The file containing rules, facts and queries")
    args = flag.parse_args()
