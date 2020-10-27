class Expression:
    def evaluate(self):
        raise NotImplemented()

    @classmethod
    def precedence(cls):
        return 0


class NumberLiteral(Expression):
    def __init__(self, num_str):
        if '.' in num_str:
            self.num = float(num_str)
        else:
            self.num = int(num_str)

    def evaluate(self):
        return self.num

    @classmethod
    def precedence(cls):
        return -1


class BinaryOp(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Plus(BinaryOp):
    def evaluate(self):
        return self.right.evaluate() + self.left.evaluate()


class Minus(BinaryOp):
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Times(BinaryOp):
    def evaluate(self):
        return self.right.evaluate() * self.left.evaluate()

    @classmethod
    def precedence(cls):
        return 1


class Divide(BinaryOp):
    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

    @classmethod
    def precedence(cls):
        return 1


class Calculator(object):
    def evaluate(self, string):
        # tokens = ('(' + string + ')').replace('', ' ').replace('  ', ' ').split()
        string = string.replace('*', ' * ').replace('+', ' + ').replace('-', ' - ').replace('/', ' / ')
        tokens = ('(' + string + ')').replace('(', ' ( ').replace(')', ' ) ').split()

        print(tokens)
        paren_expression, index = self.parse_parens(tokens, 0)
        expression = self.parse_expressions(paren_expression)
        return expression.evaluate()

    def parse_parens(self, tokens, index):
        expression = []
        assert '(' == tokens[index]
        index += 1
        while tokens[index] != ')':
            t = tokens[index]
            if t == '(':
                sub_exp, index = self.parse_parens(tokens, index)
                expression.append(sub_exp)
            elif t == ')':
                break
            else:
                expression.append(t)
                index += 1

        assert ')' == tokens[index]
        return expression, index + 1

    ops_map = {
        '+': Plus,
        '-': Minus,
        '*': Times,
        '/': Divide
    }

    @classmethod
    def find_highest_precedence_op(cls, paren_expression):
        def key_fn(i_op_char):
            _, op_char = i_op_char
            return Calculator.ops_map.get(op_char, NumberLiteral).precedence()

        return max(enumerate(paren_expression), key=key_fn)

    def parse_expressions(self, paren_expression):
        print(paren_expression)

        # do not allow '()'
        if len(paren_expression) == 0:
            raise ValueError('paren_expression can not be empty')

        # process a '(a list | a literal)' by unpacking it
        if len(paren_expression) == 1:
            if type(paren_expression[0]) is list:
                return self.parse_expressions(paren_expression[0])
            else:
                return NumberLiteral(paren_expression[0])

        expressions = paren_expression.copy()

        # process literals and subexpressions
        for i, exp in enumerate(expressions):
            if type(exp) is list:
                expressions[i] = self.parse_expressions(exp)
            elif exp not in Calculator.ops_map:
                expressions[i] = NumberLiteral(exp)

        # process the binary operators in order of precedence
        while len(expressions) > 1:
            print(expressions)
            i, exp = Calculator.find_highest_precedence_op(expressions)
            exp_cls = Calculator.ops_map[exp]
            exp = exp_cls(expressions[i - 1], expressions[i + 1])
            expressions[i-1:i+2] = [exp]

        return expressions[0]


c = Calculator()
print(c.evaluate('2 / 2 + 3 * 4 - 6'))
print(c.evaluate('2 + (1 + 3) * 4 * ((2) * (1))'))
print(c.evaluate('((((1)*2)))'))
print(c.evaluate('2 + 3 * 4 / 3 - 6 / 3 * 3 +    8'))
print(c.evaluate('1 + 1'))
print(c.evaluate('2 * (1 + 3 * (1 + 1))'))
print(c.evaluate('3 * 2 + 3'))
print(c.evaluate('3 + 3 * 3'))

# (), +, -, *, /

# 2 + 3 * 4 / 3 - 6 / 3 * 3 + 8 == 8,
