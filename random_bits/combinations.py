cache = []


def product_sum_req(elements, sublist_length, position):
    global cache

    cache_key = len(elements) * (sublist_length - 1) + position

    if cache[cache_key] != 0:
        print(cache, elements, sublist_length)
        return cache[cache_key]

    sublists = 0

    for index in range(position, len(elements) - sublist_length + 1):
        if sublist_length - 1 == 0:
            sublists += elements[index]
        else:
            sublists += elements[index] * \
                        product_sum_req(
                            elements, sublist_length - 1, index + 1)

    sublists %= 10 ** 9 + 7
    cache[cache_key] = sublists
    return sublists


def sp_rec(arr, m):
    global cache
    cache = [0] * (len(arr) * m)
    return product_sum_req(arr, m, 0)


def product_sum(arr, sublist_len):
    curr_gen = [1] * (len(arr) + 1)

    for k in range(1, sublist_len + 1):
        # print(curr_gen)
        prev_gen = curr_gen
        curr_gen = [0] * (len(arr) + 1)
        for n in range(k, len(arr) + 1):
            curr_gen[n] = (arr[n-1] * prev_gen[n-1] + curr_gen[n - 1]) %\
                          (10**9 + 7)

    # print(curr_gen, curr_gen[len(arr) - sublist_len + 1])
    return curr_gen[-1]


# sp = sp_rec
assert (product_sum([1] * 4, 1) == 4)
assert (product_sum([1, 2, 3], 1) == 6)
assert (product_sum([1, 1, 1], 2) == 3)
assert (product_sum([1, 1, 1], 3) == 1)
assert (product_sum([1, 2, 3], 2) == 11)

# import time
#
# start = time.time()
# print(sp(list(range(10 ** 2)), 14))
# end = time.time()
# print(end - start)
