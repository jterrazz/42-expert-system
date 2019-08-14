OPERATORS = ['!', '+', '|', '^', '(', ')']
PRIORITY = {'!': 4, '+': 3, '|': 2, '^': 1}


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
