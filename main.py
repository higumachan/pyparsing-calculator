from functools import reduce

from pyparsing import Word, Forward, Literal, Suppress, ZeroOrMore


def plus_minus(string, locs, tokens):
    ret = tokens[0]
    for pm, n in zip(tokens[1::2], tokens[2::2]):
        if pm == "+":
            ret += n
        elif pm == "-":
            ret -= n
    return ret


def mul(string, locs, tokens):
    return reduce(lambda acc, y: acc * y, tokens[::2], 1)


def parse_int(string, locs, tokens):
    return int(tokens[0])


num = Word("123456789", bodyChars="0123456789")
num.setParseAction(parse_int)

expr = Forward()
mul_expr = Forward()
plus_minus_expr = Forward()

mul_expr <<= expr + ZeroOrMore((Literal("*")) + expr)
mul_expr.setParseAction(mul)

plus_minus_expr <<= mul_expr + ZeroOrMore((Literal("+") | "-") + mul_expr)
plus_minus_expr.setParseAction(plus_minus)

expr <<= Suppress("(") + plus_minus_expr + Suppress(")") | num


if __name__ == '__main__':
    assert 2 == plus_minus_expr.parseString("1 + 1", True)[0]
    assert 3 == plus_minus_expr.parseString("1 + 1 * 2", True)[0]
    assert -1 == plus_minus_expr.parseString("1 - 1 * 2", True)[0]
    assert 0 == plus_minus_expr.parseString("(1 - 1) * 2", True)[0]
    assert 4 == plus_minus_expr.parseString("(1 + 1) * 2", True)[0]
    assert 4 == plus_minus_expr.parseString("2 * 2", True)[0]
    assert 3 == plus_minus_expr.parseString("1 + (1 + 1)", True)[0]
