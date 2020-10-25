import itertools

tests = [list(itertools.permutations(range(0, 10), i)) for i in range(0, 11)]


def alpha_metrics(puzzle):
    additions, answer = puzzle.split(' = ')
    additions = additions.split(' + ')

    all_chars = list({c for c in puzzle if c.isalpha()})

    def word_to_num(w, char_map):
        n = 0
        for c in w:
            n *= 10
            n += char_map[c]
            if n == 0:
                return -1
        return n

    for t in tests[len(all_chars)]:
        char_map = dict(zip(all_chars, t))
        if sum(word_to_num(a, char_map) for a in additions) == \
                word_to_num(answer, char_map):
            adds = (str(word_to_num(a, char_map)) for a in additions)
            return f"{' + '.join(adds)} = {word_to_num(answer, char_map)}"


example_tests = (
    ('TOM + JER = DON', '208 + 493 = 701'),
    ('AAA + BBB = CCC', '222 + 111 = 333'),
    ('SEND + MORE = MONEY','9567 + 1085 = 10652'),
    # ('ZEROES + ONES = BINARY','698392 + 3192 = 701584'),
    # ('COUPLE + COUPLE = QUARTET','653924 + 653924 = 1307848'),
    ('DO + YOU + FEEL = LUCKY', '57 + 870 + 9441 = 10368'),
    ('ELEVEN + NINE + FIVE + FIVE = THIRTY', '797275 + 5057 + 4027 + 4027 = 810386'),
)

for inp, out in example_tests:
    r = alpha_metrics(inp)
    print(inp, r, out)
    assert r == out, (inp, r, out)
