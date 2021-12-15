#!/usr/bin/env python
# https://adventofcode.com/2021/day/14

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
string = list(lines[0])
rules  = {i[0]: i[2] for i in [x.split(' ') for x in lines[2:]]}


###########
#  parts  #
###########


def part1(steps):
    """ Brute force approach building out the string for each iteration. """
    polymer = string.copy()
    for step in range(steps):
        # id our pairs
        pairs = []
        polymer_length = len(polymer)
        for i in range(polymer_length - 1):
            pairs.append(polymer[i] + polymer[i + 1])

        # grab the last char of last pairs
        last_bit = pairs[-1][-1]

        # modify our pairs
        for idx, val in enumerate(pairs):
            pairs[idx] = val[0] + rules[val]

        polymer = ''.join(pairs) + last_bit

    # build up a count of items in our polymer then sort by value
    d = {item: polymer.count(item) for item in polymer}
    small_to_big = [k for k, v in sorted(d.items(), key=lambda item: item[1])]

    return d[small_to_big[-1]] - d[small_to_big[0]]


def part2(steps):
    """ Tracking pairs instead. """
    # convert our rules to output the two pairs returned when transforming a pair
    rule_map = {}
    for rule, char in rules.items():
        rule_map[rule] = [rule[0] + char, char + rule[1]]

    # identify starting pairs from the seed string
    starting_pairs = [''.join(string[i:i + 2]) for i in range(len(string) - 1)]

    # count how many of each pair we have
    # eg {'CH': 1, 'HH': 0, 'CB': 1, 'NH': 1, ...}
    pairs = {}
    for pair in starting_pairs:
        pairs[pair] = pairs.get(pair, 0) + 1

    # iterate through each step, each time we only care about the counts of new pairs generated
    for i in range(steps):
        new_pairs = {}
        for pair, count in pairs.items():
            babies = rule_map[pair]
            new_pairs[babies[0]] = new_pairs.get(babies[0], 0) + (1 * count)
            new_pairs[babies[1]] = new_pairs.get(babies[1], 0) + (1 * count)

        # replace pairs with the count of pairs in the next generation
        pairs = new_pairs

    # for the last set of pairs, we only care about adding up the first letter
    # in each pair, the second will be the first in another pair except for the
    # very last character in the string which we'll manually add in later
    # eg {'C': 0, 'H': 0, 'N': 0, 'B': 0}
    counts = {}
    for pair in pairs:
        counts[pair[0]] = counts.get(pair[0], 0) + pairs[pair]

    # add in 1 for the last character in the original string, it will always be
    # last in every iteration and it gets excluded in the count done above
    counts[string[-1]] += 1

    # sort character by count
    small_to_big = [k for k, v in sorted(counts.items(), key=lambda item: item[1])]

    # do the math to subtract smallest count from largest
    return counts[small_to_big[-1]] - counts[small_to_big[0]]


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1(10))
    print('Part 2:', part2(40))
