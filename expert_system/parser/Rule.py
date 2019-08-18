from enum import Enum
import re

OPERATORS = ['!', '+', '|', '^', '(', ')']
PRIORITY = {'!': 4, '+': 3, '|': 2, '^': 1}


class ImplicationType(Enum):
    IMPLY = "=>"
    EQUAL = "<=>"


class NPIParser:
    @staticmethod
    def infix_to_postfix(formula):
        if formula.__len__() is 0:
            raise BaseException("No rules to be parsed")

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


class ExpertRule(NPIParser):
    def __init__(self, rule_str):
        splitted = re.split(r'=>|<=>', rule_str)
        self.type = (ImplicationType.EQUAL if "<=>" in rule_str else ImplicationType.IMPLY)

        left = list(splitted[0].replace(' ', ''))
        right = list(splitted[1].replace(' ', ''))

        self.npi_left = self.infix_to_postfix(left)
        self.npi_right = self.infix_to_postfix(right)

        # check if ! in conclusion exp: => !(A + B)
        if '+!' in self.npi_right:
            raise BaseException(f'Error at line : {rule_str} - Rule is badly formatted')

        # check if '|' in right exp: B | D <=> A
        if self.type == ImplicationType.EQUAL and '|' in self.npi_left:
            raise BaseException(f'Error at line : {rule_str} - Rule is badly formatted')

        # check if ! in conclusion or left, exp: D + C <=> !(A + B) OR !(A + B) <=> D + C
        if self.type == ImplicationType.EQUAL and ('+!' in self.npi_right or '+!' in self.npi_left):
            raise BaseException(f'Error at line : {rule_str} - Rule is badly formatted')

    def __repr__(self):
        return f'<ImplicationRule> left: { self.npi_left }, right: { self.npi_right }, type: { self.type }'
