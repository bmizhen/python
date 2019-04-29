import itertools
import pprint


def make_int(nums):
    sum = 0
    for i in nums:
        sum *= 10
        sum += i

    return sum


def make_list(n, num_length):
    return [int(i) for i in format(n, '0' + str(num_length))]


def fix_zero(nums):
    """Moves first non-zero digit to the front"""
    if nums[0] == 0:
        nums = nums.copy()
        # find first non-zero number and swap
        for i in range(1, len(nums)):
            if nums[i] > 0:
                nums[0], nums[i] = nums[i], nums[0]
                return nums
    return nums


def terminate(iteration, nums, num_length):
    nums_ascending = fix_zero(sorted(nums))
    nums_descending = sorted(nums, reverse=True)
    high = make_int(nums_descending)
    low = make_int(nums_ascending)

    result = make_list(high - low, num_length)
    if sorted(result) == nums_ascending:
        # we found terminating number
        return iteration, high - low
    else:
        print(iteration, high, low, high - low, make_int(result))
        return terminate(iteration + 1, result, num_length)[0], \
               high - low  # this is the first difference


def number_generator(num_length):
    for number in range(10 ** (num_length - 1), 10 ** num_length - 1):
        numbers = make_list(number, num_length)
        for digit in numbers[1:]:
            if digit != numbers[0]:
                # we found a digit that is different from the first
                # therefore not all digits are the same
                yield numbers
                break


def try_numbers(num_length):
    first_diff_map = {}

    for n in number_generator(num_length):
        iterations, diff = terminate(0, n, num_length)
        # make a map of [first difference -> number of iterations]
        # the first difference is the first recursive call
        first_diff_map[make_int(sorted(make_list(diff, num_length)))] = iterations
        print(iterations, "\n")

    pprint.pprint(first_diff_map)

    diff = sorted(first_diff_map.items(), key=lambda x: x[1])
    for n in itertools.groupby(diff, lambda x: x[1]):
        # group the first differences by the total number of iterations
        print(n[0], list(n[1]))


# run the alg for numbers of length 4
try_numbers(4)

