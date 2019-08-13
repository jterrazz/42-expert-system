import re

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

tmp = '! ( A + B ) ^ ( D | K )'
tmp = re.split('\s', tmp)
infix_to_postfix(tmp)