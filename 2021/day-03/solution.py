#!/usr/bin/env python
# https://adventofcode.com/2021/day/3

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()


###########
#  parts  #
###########


def part1():
    # make a new bits array containing arrays of each positional bit
    # eg [[0,1,1,0,1,0,...], [1,1,0,1,0,0,...], ...]
    bits = [[], [], [], [], [], [], [], [], [], [], [], []]
    for line in lines:
        for i, v in enumerate(line):
            bits[i].append(v)

    # look for most frequent entry of each bits and append it to binary string
    gamma_rate_bin_string = ''
    for bit in bits:
        gamma_rate_bin_string += max(set(bit), key=bit.count)

    # now repeat looking for epsilon rate, we could just invert the binary of gamma_rate_bin_string, but it's late and i'm tired
    epsilon_rate_bin_string = ''
    for bit in bits:
        epsilon_rate_bin_string += min(set(bit), key=bit.count)

    print(gamma_rate_bin_string)
    print(epsilon_rate_bin_string)
    print(int(gamma_rate_bin_string, 2) * int(epsilon_rate_bin_string, 2))


def part2():
    oxygen = lines.copy()
    while len(oxygen) != 1:
        for bit in range(12):
            bits = []
            for line in oxygen:
                bits.append(line[bit])
            ones = bits.count('1')
            zeros = bits.count('0')
            if zeros > ones:
                keep = '0'
            else:
                keep = '1'

            oxygen = [x for x in oxygen if x[bit] == keep]

    co2 = lines.copy()
    while len(co2) != 1:
        for bit in range(12):
            # TODO: this is not efficent, we have to complete our for bit loop
            # even if we are at a length of one on bit 2, python does not allow
            # multi-layer breaks, so need to refactor to put this in a func and
            # just return
            if len(co2) == 1:
                break
            bits = []
            for line in co2:
                bits.append(line[bit])
            ones = bits.count('1')
            zeros = bits.count('0')
            if zeros > ones:
                keep = '1'
            else:
                keep = '0'

            co2 = [x for x in co2 if x[bit] == keep]

    print(oxygen)
    print(co2)
    print(int(oxygen[0], 2) * int(co2[0], 2))


##########
#  main  #
##########


if __name__ == "__main__":
    part1()
    print('---')
    part2()
