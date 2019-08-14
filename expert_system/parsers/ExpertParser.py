import re
from .NPIParser import NPIParser


class ExpertParser(NPIParser):
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.postfix = None
        self.rules_postfix = None

        self.parse_input()

        #  TODO TMP, Below self.rules need to be set by the parse_input() ft
        self.rules = re.split('\s', '! ( A + B ) ^ ( D | K )')

        self.set_rules_postfix()

    def set_rules_postfix(self):
        self.rules_postfix = self.infix_to_postfix(self.rules)

    def parse_input(self):
        input_lines = [x.strip() for x in self.raw_input]
        input_lines = list(filter(None, input_lines))

        if self.ft_parser(input_lines) is False:
            raise BaseException("Parsing failed") # Replace by detailled message Error ?

    @staticmethod
    def ft_split_operators(formula):
        return re.split(r'!|\||\+|\^|', formula)

    @staticmethod
    def ft_check_parentheses(rule):
       return rule.count("(") == rule.count(")")

    @staticmethod
    def ft_all_atoms(rules):
        atoms = []
        for elem in rules:
            atoms = atoms + list(filter(None, re.split(r'\s|!|\+|\^|=>|\||<=>|=|>|<|\(|\)', elem)))
        return atoms

    @staticmethod
    def ft_check_facts_in_list_atoms(atoms, facts):
        fact = list(filter(None, re.split('=', facts)))
        if fact:
            fact = list(fact[0])
        for elem in fact:
            if elem not in atoms:
                return False
        return True

    @staticmethod
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

    @staticmethod
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
                atoms = ExpertParser.ft_all_atoms(rules)
                fact -= 1
                if fact < 0 or queries <= 0 or regex_fact.match(elem) is None or not ExpertParser.ft_check_facts_in_list_atoms(atoms, elem):
                    print('Error format line: {}'.format(elem))
                    return False
            elif elem[0] == '?':
                queries -= 1
                if fact > 0 or regex_queries.match(elem) is None or not ExpertParser.ft_check_queries_in_list_atoms(atoms, elem):
                    print('Error format line: {}'.format(elem))
                    return False
            else:
                rule -= 1
                if fact <= 0 or queries <= 0 or regex_rule.match(elem) is None or not ExpertParser.ft_check_parentheses(elem):
                    print('Error format line: {}'.format(elem))
                    return False
                else:
                    rules += elem
            if elem[0] != '=' and elem[0] != '?':
                print(re.split(r'=>|<=>', elem)[0])
        if fact > 0 or queries > 0 or rule > 0:
            return False
        return True
