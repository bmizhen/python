from itertools import filterfalse

def partition(p, it):
    l = list(it)

    return filter(p, l), filterfalse(p, l)


def chain_iterables(*iterables):
    for it in iterables:
        yield from it


def qsort(items):
    it = iter(items)

    try:
        x = next(it)
    except StopIteration:
        return []

    less_than_x, not_less_than_x = partition(lambda y: x > y, it)

    return chain_iterables(
        qsort(less_than_x),
        [x],
        qsort(not_less_than_x))


import random

for i in range(1000):
    l = [random.randrange(-20, 20) for _ in range(50)]
    assert list(qsort(l)) == list(sorted(l))

print(list(qsort([9,8,7,6,5,4,3,2,1])))
