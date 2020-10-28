import re


class TokenQueue:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        if self.index == len(self.tokens):
            return None
        return self.tokens[self.index]

    def pop(self):
        self.index += 1
        return self.tokens[self.index - 1]

    def get(self):
        return self.tokens[self.index:]

    def __str__(self):
        return str(self.get())


class Compiler(object):

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    def tokenize(self, program):
        print(program)
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1_fn(self, tq: TokenQueue):
        if tq.peek() == '[':
            tq.pop()
            args = self.parse_arg_list([], tq)
            assert tq.pop() == ']'
        else:
            args = []
        expression = self.parse_expression(tq, args)
        return expression

    def pass1(self, program):
        """Returns an un-optimized AST"""
        # print(program)
        tokens = self.tokenize(program)
        # print(tokens)
        ast = self.pass1_fn(TokenQueue(tokens))
        # print(ast)
        return ast

    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        return self.eval(ast)

    def eval(self, ast):
        op = ast['op']
        if op in {'imm', 'arg'}:
            return ast
        a = self.eval(ast['a'])
        b = self.eval(ast['b'])

        if a['op'] == 'imm' and b['op'] == 'imm':
            return {'op': 'imm', 'n': self.calc(op, a['n'], b['n'])}
        else:
            return {'op': op, 'a': a, 'b': b}

    def parse_arg_list(self, args_so_far, tq):
        if tq.peek() == ']':
            return args_so_far
        else:
            args_so_far.append(tq.pop())
            return self.parse_arg_list(args_so_far, tq)

    def parse_expression(self, tq, args):
        # print('parse_expression', tq)
        term_a = self.parse_term(tq, args)
        while tq.peek() and tq.peek() != ')':
            op = tq.pop()
            term_b = self.parse_term(tq, args)
            term_a = {'op': op, 'a': term_a, 'b': term_b}

        return term_a

    def parse_term(self, tq, args):
        # print('parse_term', tq)
        factor = self.parse_factor(tq, args)
        # print('factor:', factor)
        if not tq.peek():
            return factor

        while tq.peek() in {'*', '/'}:
            op = tq.pop()
            # print('op', op)
            factor = {'op': op, 'a': factor, 'b': self.parse_factor(tq, args)}
        return factor

    def parse_factor(self, tq, args):
        # print('parse_factor', tq)
        f = tq.pop()
        if f == '(':
            f = self.parse_expression(tq, args)
            # print('factor->expression:', f)
            assert tq.pop() == ')'
            return f
        if type(f) == int:
            # print('factor->value:', f)
            return {'op': 'imm', 'n': int(f)}
        print('factor->arg:', f, args.index(f), args)
        return {'op': 'arg', 'n': args.index(f)}

    def calc(self, op, a, b):
        if '+' == op:
            return a + b
        if '*' == op:
            return a * b
        if '-' == op:
            return a - b
        if '/' == op:
            return a // b
        raise ValueError('op can\'t be', op, a, b)

    def pass3(self, ast):
        """Returns assembly instructions"""
        assembly = []
        self.asm(ast, assembly)
        return assembly

    def asm(self, op, assembly):
        if op['op'] == 'imm':
            assembly.append(f"IM {op['n']}")
        elif op['op'] == 'arg':
            assembly.append(f"AR {op['n']}")
        else:
            self.asm(op['a'], assembly)
            assembly.append(f"PU")
            self.asm(op['b'], assembly)
            assembly.append('SW')
            assembly.append('PO')
            op_map = {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}
            assembly.append(op_map[op['op']])



"""
    function   ::= '[' arg-list ']' expression

    arg-list   ::= /* nothing */
                 | variable arg-list

    expression ::= term
                 | expression '+' term
                 | expression '-' term

    term       ::= factor
                 | term '*' factor
                 | term '/' factor

    factor     ::= number
                 | variable
                 | '(' expression ')'
"""
import pprint

pprint.pprint(Compiler().compile('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'))

pprint.pprint(Compiler().compile('1'))
print()
pprint.pprint(Compiler().compile('1 * 1 + 1'))

print()
pprint.pprint(Compiler().compile('1 * (1 + 1)'))

print()
pprint.pprint(Compiler().compile('[a] a * 1 / a * 2'))

# [ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)
pprint.pprint({'op': '/',
               'a': {'op': '*',
                     'a': {'op': '*',
                           'a': {'op': 'imm', 'n': 2},
                           'b': {'op': 'imm', 'n': 3}},
                     'b': {'op': '+',
                           'a': {'op': 'arg', 'n': 0},
                           'b': {'op': '-',
                                 'a': {'op': '*',
                                       'a': {'op': 'imm',
                                             'n': 5},
                                       'b': {'op': 'arg',
                                             'n': 1}},
                                 'b': {'op': '*',
                                       'a': {'op': 'imm', 'n': 3},
                                       'b': {'op': 'arg', 'n': 2}}}}},
               'b': {'op': '+',
                     'a': {'op': 'imm', 'n': 1},
                     'b': {'op': '+', 'a': {'op': 'imm', 'n': 3},
                           'b': {'op': '*',
                                 'a': {'op': 'imm', 'n': 2},
                                 'b': {'op': 'imm', 'n': 2}}}}})

pprint.pprint(Compiler().compile('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'))
pprint.pprint(Compiler().compile('[ x y z ] x - y - z + 10 / 5 / 2 - 7 / 1 / 7'))
