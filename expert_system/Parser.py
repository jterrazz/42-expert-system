import re
import sys

from expert_system.helper.Color import Ft_colors

OPERATORS = ['!', '+', '|', '^', '(', ')']
PRIORITY = {'!': 4, '+': 3, '|': 2, '^': 1}

def infix_to_postfix(formula):
    stack = [] # only pop when the coming op has priority
    output = ''
    for ch in formula:
        if ch not in OPERATORS:
            output += ch
        elif ch == '(':
            stack.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop() # pop '('
        else:
            while stack and stack[-1] != '(' and ch != '!' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(ch)

    # leftover
    while stack:
        output += stack.pop()
    # deduct not '!!'
    output = output.replace('!!', '')
    return output

def ft_split_operators(formula):
    return re.split(r'!|\||\+|\^|', formula)

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
    regex_rule = re.compile(r"(^((\()*(!){0,2})*[A-Z](\))*((\s*[(+|^\|)]\s*((\()*(!){0,2})*[A-Z](\))*)*)?\s*(=>|<=>)\s*((\()*(!){0,2})*[A-Z](\))*((\s*[(+|^\|)]\s*((\()*(!){0,2})*[A-Z](\))*)*)?\s*$)")
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
        if elem[0] != '=' and elem[0] != '?':
            print(re.split(r'=>|<=>', elem)[0])
    if fact > 0 or queries > 0 or rule > 0:
        return False
    return True

# Main Function
if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000)
    except:
        print('Error opening file for reading ..!!')
        # If error expect does the program stops ???

    content = [x.strip() for x in content]
    # filter backend lines
    content = list(filter(None, content))

    bcolors = Ft_colors()
    if ft_parser(content):
        print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "KO" + bcolors.ENDC)
