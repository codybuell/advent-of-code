#!/usr/bin/env python
# https://adventofcode.com/2021/day/18

import re

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()


###########
#  funcs  #
###########


def add_snailfish(a: str, b: str) -> str:
    # concatenate into a new 'list'
    return '[' + a + ',' + b + ']'


def explode_snailfish(a: str) -> str:
    # track count of right brackets, if we found 4 deep, and indexes
    rbraq = 0
    found = False
    start = 0
    end   = 0

    # find start and stop of a 4 deep pair
    for i, c in enumerate(a):
        if not found:
            if c == '[':
                rbraq += 1
            if c == ']':
                rbraq -= 1
            if rbraq == 5:
                found = True
                start = i
        elif c == ']':
            end = i
            break

    # exlpode it
    if found:
        # converst our exploding chunk into numbers
        numbers = [int(x) for x in (a[start + 1:end]).split(',')]

        # add lhs to first number left of, reverse things because I'm lazy
        lhs = a[0:start][::-1]
        prev_nums = re.search(r"\d+", lhs)
        if prev_nums:
            p = int(prev_nums[0][::-1])
            pp = p + numbers[0]
            lhs = re.sub(r"\d+", str(pp)[::-1], lhs, 1)
        lhs = lhs[::-1]

        # add rhs to first number right of
        rhs = a[end + 1:]
        next_nums = re.search(r"\d+", rhs)
        if next_nums:
            n = int(next_nums[0])
            nn = n + numbers[1]
            rhs = re.sub(r"\d+", str(nn), rhs, 1)

        # replace original expression with a 0
        return lhs + '0' + rhs


def split_snailfish(a: str) -> str:
    # build an array of numbers in our string
    numbers = [int(x) for x in re.findall(r"\d+", a)]

    # find numbers that need splitting
    need_splitting = [x for x in numbers if x > 9]

    # if none then stop
    if need_splitting:
        to_split = need_splitting[0]
        lhs = to_split // 2
        rhs = lhs + (to_split % 2)
        return re.sub(str(to_split), '[' + str(lhs) + ',' + str(rhs) + ']', a, 1)


def reduce_snailfish(a: str) -> str:
    # try exploding first (has nested pair 4 deep)
    a_splode = explode_snailfish(a)
    if a_splode is not None:
        return a_splode

    # try splitting next, has regular number > 10
    a_split = split_snailfish(a)
    if a_split is not None:
        return a_split

    # else just hand the string back
    return a


def get_magnitude(a: list) -> int:
    # grab the left and right sides
    lhs = a[0]
    rhs = a[1]

    # if either side is a list, recurse into it
    if type(lhs) == list:
        lhs = get_magnitude(lhs)
    if type(rhs) == list:
        rhs = get_magnitude(rhs)

    # now we have numbers, do the math and return
    return (lhs * 3) + (rhs * 2)


###########
#  parts  #
###########


def part1():
    # start with our first line
    sum = lines[0]

    # add next line and reduce
    for line in lines[1:]:
        sum = add_snailfish(sum, line)
        while True:
            snap = sum
            sum = reduce_snailfish(sum)
            if sum == snap:
                break

    # convert to an actual list and get magnitude
    as_list = eval(sum)
    return get_magnitude(as_list)


def part2():
    # determine how many lines we need to add
    length = len(lines)

    # get possible index combinations
    combos = []
    for a in range(length):
        for b in range(length):
            combos.append([a, b])

    # collect all magnitudes
    magnitudes = []
    for combo in combos:
        # don't add a starfish number against itself
        if combo[0] == combo[1]:
            continue
        sum = add_snailfish(lines[combo[0]], lines[combo[1]])
        while True:
            snap = sum
            sum = reduce_snailfish(sum)
            if sum == snap:
                break
        as_list = eval(sum)
        magnitudes.append(get_magnitude(as_list))

    # return back the biggest magnitude
    return max(magnitudes)


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
