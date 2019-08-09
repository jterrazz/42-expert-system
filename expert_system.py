import re
import sys

class Ft_colors:
    PURPLE = '\x1b[94m'
    OKBLUE = '\x1b[96m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    UNDERLINE = '\x1b[4m'

def ft_check_parentheses(rule):
   return rule.count("(") == rule.count(")")

def ft_all_atoms(rules):
    atoms = []
    for elem in rules:
        atoms = atoms + list(filter(None, re.split(r'\s|!|\+|\^|=>|\||<=>|=|>|<|\(|\)', elem)))
    return atoms

def ft_check_facts_in_list_atoms(atoms, facts):
    fact = list(filter(None, re.split('=', facts)))
    if fact:
        fact = list(fact[0])
    for elem in fact:
        if elem not in atoms:
            return False
    return True

def ft_check_queries_in_list_atoms(atoms, queries):
    querie = list(filter(None, re.split('\?', queries)))
    if querie:
        querie = list(querie[0])
    else:
        return False
    for elem in querie:
        if elem not in atoms:
            return False
    return True

def ft_parser(content_file):
    regex_rule = re.compile(r"(^(\()*(!)?(\()*[A-Z](\))*((\s*[(+|^\|)]\s*(\()*(!)?(\()*[A-Z](\))*)*)?\s*(=>|<=>)\s*(\()*(!)?(\()*[A-Z](\))*((\s*[(+|^\|)]\s*(\()*(!)?(\()*[A-Z](\))*)*)?\s*$)")
    # regex_rule = re.compile(r"(^(\()*(!)?(\()*[A-Z](\))*\s+[(+|^\|)]\s+(\()*(!)?(\()*[A-Z](\))*((\s+[(+|^\|)]\s+(\()*(!)?(\()*[A-Z](\))*)*)?\s+(=>|<=>)\s(\()*(!)?(\()*[A-Z](\))*((\s+[(+|^\|)]\s+(\()*(!)?(\()*[A-Z](\))*)*)?$)")
    regex_fact = re.compile(r"(^=[A-Z]*$)")
    regex_queries = re.compile(r"(^\?[A-Z]*$)")

    fact = 1
    queries = 1
    rule = 1
    atoms = []
    rules = []
    for elem in content_file:
        elem = elem.split("#", 1)[0]
        if not elem:
            continue
        if elem[0] == '=':
            atoms = ft_all_atoms(rules)
            fact -= 1
            if fact < 0 or queries <= 0 or regex_fact.match(elem) is None or not ft_check_facts_in_list_atoms(atoms, elem):
                print('Error format line: {}'.format(elem))
                return False
        elif elem[0] == '?':
            queries -= 1
            if fact > 0 or regex_queries.match(elem) is None or not ft_check_queries_in_list_atoms(atoms, elem):
                print('Error format line: {}'.format(elem))
                return False
        else:
            rule -= 1
            if fact <= 0 or queries <= 0 or regex_rule.match(elem) is None or not ft_check_parentheses(elem):
                print('Error format line: {}'.format(elem))
                return False
            else:
                rules += elem
    if fact > 0 or queries > 0 or rule > 0:
        return False
    return True

# Main Function
if __name__ == "__main__":
   try:
       with open(sys.argv[1]) as f:
           content = f.readlines()
   except:
       print('Error opening file for reading ..!!')

   content = [x.strip() for x in content]
   # filter backend lines
   content = list(filter(None, content))

   bcolors = Ft_colors()
   if ft_parser(content):
       print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
   else:
       print(bcolors.FAIL + "KO" + bcolors.ENDC)
