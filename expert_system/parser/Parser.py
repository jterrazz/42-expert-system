import re
from .Rule import ExpertRule


class ExpertParser:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.raw_rules = []
        self.structured_rules = []
        self.facts = []
        self.queries = []

        self.ft_parser()
        self.set_structured_rules()

    def set_structured_rules(self):
        for raw_rule in self.raw_rules:
            self.structured_rules.append(ExpertRule(raw_rule))

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
        fact = list(filter(None, re.split(r'=|\s', facts)))
        if fact:
            fact = list(fact[0])
        for elem in fact:
            if elem not in atoms:
                return False
        return True

    @staticmethod
    def ft_check_queries_in_list_atoms(atoms, queries):
        query = list(filter(None, re.split(r'\?|\s', queries)))
        if query:
            query = list(query[0])
        else:
            return False
        for elem in query:
            if elem not in atoms:
                return False
        return True

    def ft_parser(self):
        input_lines = [x.strip() for x in self.raw_input]
        content_file = list(filter(None, input_lines))

        regex_rule = re.compile(r"(^((\()*(\s)*(!){0,2})*(\s)*[A-Z](\s)*(\))*((\s*[(+|^)]\s*((\()*(\s)*(!){0,2})*(\s)*[A-Z](\s)*(\))*)*)?\s*(=>|<=>)\s*((\()*(\s)*(!){0,2})*[A-Z](\s)*(\))*((\s*[(+)]\s*((\()*(\s)*(!){0,2})*(\s)*[A-Z](\s)*(\))*)*)?\s*$)")
        regex_fact = re.compile(r"(^=[A-Z]*(\s)*$)")
        regex_queries = re.compile(r"(^\?[A-Z]*(\s)*$)")

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
                if fact < 0:
                    raise BaseException(f'Error at line : {elem} - Facts were already defined line')
                if queries <= 0:
                    raise BaseException(f'Error at line : {elem} - Facts must be defined before queries')
                if not ExpertParser.ft_check_facts_in_list_atoms(atoms, elem):
                    raise BaseException(f'Error at line : {elem} - A fact was defined but not found in the rules')
                if regex_fact.match(elem) is None:
                    raise BaseException(f'Error at line : {elem} - Fact badly formatted')
            elif elem[0] == '?':
                queries -= 1
                if fact > 0:
                    raise BaseException(f'Error at line : {elem} - Facts were not defined')
                if regex_queries.match(elem) is None:
                    raise BaseException(f'Error at line : {elem} - Queries badly formatted')
                if not ExpertParser.ft_check_queries_in_list_atoms(atoms, elem):
                    raise BaseException(f'Error at line : {elem} - An atom in the queries was not defined in the rules')
            else:
                rule -= 1
                if fact <= 0:
                    raise BaseException(f'Error at line : {elem} - Rules must be defined before facts')
                if queries <= 0:
                    raise BaseException(f'Error at line : {elem} - Rules must be defined before queries')
                if regex_rule.match(elem) is None:
                    raise BaseException(f'Error at line : {elem} - Rule is badly formatted')
                if not ExpertParser.ft_check_parentheses(elem):
                    raise BaseException(f'Error at line : {elem} - Rule has badly formatted parentheses')
                else:
                    rules += elem

            if elem[0] != '=' and elem[0] != '?':
                self.raw_rules.append(elem)
            else:
                if elem[0] == '=':
                    self.facts = list(elem.replace('=', '').replace(' ', '').replace("\t", ""))
                else:
                    self.queries = list(elem.replace('?', '').replace(' ', '').replace("\t", ""))
        if fact > 0 or queries > 0 or rule > 0:
            raise BaseException("Missing one of facts, queries or rules")
