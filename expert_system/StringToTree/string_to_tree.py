import re

class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)

def print_tree_inorder(tree):
    if tree is None:
        return
    print_tree_inorder(tree.left)
    print(tree.cargo, end=" ")
    print_tree_inorder(tree.right)


OPERATORS = ['!', '+', '|', '^', '(', ')']
PRIORITY = {'+': 3, '|': 2, '^': 1}

def infix_to_postfix(formula):
    stack = []  # only pop when the coming op has priority
    output = []
    nott = []
    for ch in formula:
        if ch == '!':
            if nott and nott[-1] == '!':
                nott.pop()  # pop '!!'
            else:
                nott.append('!')
        elif ch not in OPERATORS:
            output.append(ch)
            if nott and nott[-1] != '(':
                output.append('!')
                nott.pop()
        elif ch == '(':
            stack.append('(')
            if nott: nott.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # pop '('
            if nott:
                output.append('!')
                nott = []
        else:
            while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output.append(stack.pop())
            stack.append(ch)
    while stack:
        output.append(stack.pop())
    return output

tmp = '! ( ! C ) + B'
tmp = re.split('\s', tmp)
output = infix_to_postfix(tmp)
print(output)

# EXAMPLE: A | B + C
def postfix_to_tree(formula):
    for x in formula[::-1]:
        print(x, end='')
        tree = Tree(x, postfix_to_tree())
    return tree
# tree = Tree("|", Tree("+", Tree('C'), Tree('B')), Tree('A'))
# print_tree_inorder(postfix_to_tree(output))