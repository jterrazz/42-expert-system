import re
from .NPIParser import NPIParser
from enum import Enum


class ImplicationType(Enum):
    IMPLY = "=>"
    EQUAL = "<=>"


class ImplicationRule(NPIParser):
    def __init__(self, rule_str):
        splitted = re.split(r'=>|<=>', rule_str)
        self.type = (ImplicationType.IMPLY if "=>" in rule_str else ImplicationType.EQUAL)

        left = list(splitted[0].replace(' ', ''))
        right = list(splitted[1].replace(' ', ''))

        self.npi_left = self.infix_to_postfix(left)
        self.npi_right = self.infix_to_postfix(right)

    def __repr__(self):
        return f'<ImplicationRule> left: { self.npi_left }, right: { self.npi_right }, type: { self.type }'


class ExpertParser:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.raw_rules = []
        self.structured_rules = []

        self.ft_parser() # set self.raw_rules
        self.set_structured_rules()

    def set_structured_rules(self):
        # self.raw_rules = ["A + B => C"]
        for raw_rule in self.raw_rules:
            self.structured_rules.append(ImplicationRule(raw_rule))

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

    def ft_parser(self):
        input_lines = [x.strip() for x in self.raw_input]
        content_file = list(filter(None, input_lines))

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
                    raise BaseException(f'Error format line: {elem}')
            elif elem[0] == '?':
                queries -= 1
                if fact > 0 or regex_queries.match(elem) is None or not ExpertParser.ft_check_queries_in_list_atoms(atoms, elem):
                    raise BaseException(f'Error format line: {elem}')
            else:
                rule -= 1
                if fact <= 0 or queries <= 0 or regex_rule.match(elem) is None or not ExpertParser.ft_check_parentheses(elem):
                    raise BaseException(f'Error format line: {elem}')
                else:
                    rules += elem

            if elem[0] != '=' and elem[0] != '?':
                self.raw_rules.append(elem)
        if fact > 0 or queries > 0 or rule > 0:
            raise BaseException("Missing one of facts, queries or rules")
