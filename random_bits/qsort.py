from itertools import filterfalse

def partition(p, it):
    items = list(it)
    return filter(p, items), filterfalse(p, items)

def chain_iterables(*iterables):
    for it in iterables:
        yield from it


def qsort_iter(items):
    it = iter(items)

    try:
        x = next(it)
    except StopIteration:
        return []

    less_than_x, not_less_than_x = partition(lambda y: x > y, it)

    return chain_iterables(
        qsort_iter(less_than_x),
        [x],
        qsort_iter(not_less_than_x))


def qsort_list(items):
    if not items:
        return []

    head, tail = items[0], items[1:]

    less_than_head, not_less_than_head = partition(lambda y: head > y, tail)

    return qsort_list(list(less_than_head)) + \
        [head] + \
        qsort_list(list(not_less_than_head))


import random


def test(qsort):
    for i in range(1000):
        l = [random.randrange(-20, 20) for _ in range(50)]
        assert list(qsort(l)) == list(sorted(l))


test(qsort_list)
test(qsort_iter)

print(list(qsort_iter([9,8,7,6,5,4,3,2,1])))
