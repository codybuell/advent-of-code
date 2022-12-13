#!/usr/bin/env python3
# https://adventofcode.com/2022/day/13

import os

from copy import deepcopy

################################################################################
##                                                                            ##
##  Prep Data                                                                 ##
##                                                                            ##
################################################################################

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# group packet pairs and transform from string -> arrays
packet_pairs = [[]]
packets_raw  = []
for line in lines:
    if line == '':
        packet_pairs.append([])
        continue
    packet_pairs[-1].append(eval(line))
    packets_raw.append(eval(line))


################################################################################
##                                                                            ##
##  Functions                                                                 ##
##                                                                            ##
################################################################################


def compare_pairs(pairs: list) -> bool:
    pair_1 = pairs[0]
    pair_2 = pairs[1]

    undecided = True

    while undecided:
        # check if there are any items left to pop
        len_left  = len(pair_1)
        len_right = len(pair_2)
        if len_left == 0 and len_right > 0:
            return True
        if len_left > 0 and len_right == 0:
            return False
        if len_left == 0 and len_right == 0:
            return None

        left  = pair_1.pop(0)
        right = pair_2.pop(0)

        types   = [left.__class__.__name__, right.__class__.__name__]
        typeset = set(types)

        # dealing only with ints
        if 'list' not in typeset:
            if left < right:
                return True
            if left == right:
                continue
            if left > right:
                return False

        # dealing only with lists
        if 'int' not in typeset:
            response = compare_pairs([left, right])
            if response is not None:
                return response
            continue

        # dealing withed mixed set
        new_pairs   = [left, right]
        integer_idx = types.index('int')
        new_list    = []
        new_list.append(new_pairs[integer_idx])
        new_pairs[integer_idx] = new_list
        response = compare_pairs(new_pairs)
        if response is not None:
            return response


def bubble_sort(array):
    n = len(array)

    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if not compare_pairs([deepcopy(array[j]), deepcopy(array[j + 1])]):
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break

    return array


################################################################################
##                                                                            ##
##  Part 1                                                                    ##
##                                                                            ##
################################################################################

count = 0
for idx, pair in enumerate(packet_pairs):
    right_order = compare_pairs(pair)
    index = idx + 1
    # print(str(index) + ':', right_order)
    if right_order:
        count += index

print('part 1:', count)

################################################################################
##                                                                            ##
##  Part 2                                                                    ##
##                                                                            ##
################################################################################

# append divider packets
packets_raw.extend([[[2]], [[6]]])
sorted = bubble_sort(packets_raw)
print('part 2:', (sorted.index([[2]]) + 1) * (sorted.index([[6]]) + 1))
