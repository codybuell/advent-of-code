#!/usr/bin/env python
# https://adventofcode.com/2021/day/8

# 7 Segment Truth Table
#
#   #    len     segments    missing
#   0     6      abc efg        d
#   1     2*       c  f      ab de g        aaaa
#   2     5      a cde g      b   f        b    c
#   3     5      a cd fg      b  e         b    c
#   4     4*      bcd f      a   e g        dddd
#   5     5      ab d fg       c e         e    f
#   6     6      ab defg       c           e    f
#   7     3*     a c  f       b de g        gggg
#   8     7*     abcdefg
#   9     6      abcd fg         e


import re


###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
data = []
p = re.compile(r"(^[^|]+) \| (.*$)")
for line in lines:
    match = re.match(p, line)
    data.append({
        'signals': match.group(1).split(),
        'outputs': match.group(2).split()
    })


###########
#  funcs  #
###########


def map_known_numbers(digit: str, num_map: list, six_digits: list):
    digit_len = len(digit)
    if digit_len == 2:
        num_map[1] = digit
    if digit_len == 4:
        num_map[4] = digit
    if digit_len == 3:
        num_map[7] = digit
    if digit_len == 7:
        num_map[8] = digit

    if digit_len == 6:
        six_digits.append(digit)


###########
#  parts  #
###########


def part1():
    unique_sizes = [2, 4, 3, 7]
    count = 0
    for line in data:
        for output in line['outputs']:
            if len(output) in unique_sizes:
                count += 1

    return count


def part2():
    # each line has to be decoded separately... seems the wires get mixed up every time...
    # also decode only the signals, you need to know the segment maps as
    # segments are re-arranged in the outputs... also signals has an entry for every num 0-9
    sum = 0
    for line in data:

        ######################
        #  define some vars  #
        ######################

        signals = line['signals']
        outputs = line['outputs']

        num_map = [
            '',              # 0
            '',              # 1
            '',              # 2
            '',              # 3
            '',              # 4
            '',              # 5
            '',              # 6
            '',              # 7
            '',              # 8
            ''               # 9
        ]

        segment_map = [
            '',              # normally a   -   aaaa
            '',              # normally b   -  b    c
            '',              # normally c   -  b    c
            '',              # normally d       dddd
            '',              # normally e      e    f
            '',              # normally f   -  e    f
            '',              # normally g       gggg
        ]

        six_digits = []

        ########################
        #  decode segment map  #
        ########################

        # map known numbers in signal and output
        for digit in signals:
            map_known_numbers(digit, num_map, six_digits)

        # with 1 & 7 we can id segment a
        segment_map[0] = [i for i in num_map[7] if i not in num_map[1]][0]

        # find possible c, d, & e values by looking at len 6 digits
        possible_c_d_e = [i for i in six_digits[2] if i not in six_digits[1]][0]
        possible_c_d_e += [i for i in six_digits[0] if i not in six_digits[2]][0]
        possible_c_d_e += [i for i in six_digits[1] if i not in six_digits[0]][0]

        # now we know possible c,d,e segments we can diff it with 1 to find seg f
        segment_map[5] = [i for i in num_map[1] if i not in possible_c_d_e][0]

        # now we know segments a and f we can determine segment c from num 7
        af = segment_map[0] + segment_map[5]
        segment_map[2] = [i for i in num_map[7] if i not in af][0]

        # if we know f we can id number 2 as it's only number missing f, and then we can subsequently know b
        num_map[2] = [i for i in signals if segment_map[5] not in i][0]
        twoplusf = num_map[2] + segment_map[5]
        segment_map[1] = [i for i in 'abcdefg' if i not in twoplusf][0]

        # now we know c we can find six as it's the only six digit missing that segment
        # and we can remove six from six segments leaving us with 0 and 9 in six segments
        zero_or_nine = []
        for j in six_digits:
            if segment_map[2] not in j:
                num_map[6] = j
            else:
                zero_or_nine.append(j)

        # also 5 is the only other number missing segment c
        # and af it's not missing segment c or is number 2 which we know, it's 3
        for sig in signals:
            if len(sig) == 5:
                if segment_map[2] not in sig:
                    num_map[5] = sig
                elif sig != num_map[2]:
                    num_map[3] = sig

        # diff 2 from 3 to get us segment e
        segment_map[4] = [i for i in num_map[2] if i not in num_map[3]][0]

        # 9 is the only 6 segment missing segment e
        num_map[9] = [j for j in signals if len(j) == 6 and segment_map[4] not in j][0]

        # last remaining number is 0, and 0 is only mising segment d
        num_map[0] = [j for j in signals if j not in num_map][0]
        segment_map[3] = [j for j in 'abcdefg' if j not in num_map[0]][0]

        # only unknown segment is g
        segment_map[6] = [j for j in 'abcdefg' if j not in segment_map][0]

        # alphabetize segments in our number map
        alphabetized_num_map = {}
        for idx, number in enumerate(num_map):
            alphabetized_num_map[''.join(sorted(number))] = str(idx)

        ###################
        #  decode output  #
        ###################

        value = ''
        for digit in outputs:
            value += alphabetized_num_map[''.join(sorted(digit))]

        sum += int(value)

    return sum


def diff(a: str, b: str) -> str:
    # run a bitwise xor
    return f'{(int(a, 2) ^ int(b, 2)):07b}'


def andd(a: str, b: str) -> str:
    # run a bitwise and
    return f'{(int(a, 2) & int(b, 2)):07b}'


def orrr(a: str, b: str) -> str:
    # run a bitwise or
    return f'{(int(a, 2) | int(b, 2)):07b}'


def get_if_count(vals: list, count: int) -> str:
    return [x for x in vals if x.count('1') == count][0]


def part2_binary_method():
    sum = 0

    for line in data:

        #################
        #  define vars  #
        #################

        # grab our data for the line
        signals = line['signals']
        outputs = line['outputs']

        # transform each chunk into a 7 bit string ordered a -> g
        bin_signals = []
        bin_outputs = []
        for chunk in signals:
            bin_signals.append(''.join(['1' if x in chunk else '0' for x in 'abcdefg']))
        for chunk in outputs:
            bin_outputs.append(''.join(['1' if x in chunk else '0' for x in 'abcdefg']))

        # define placeholders for decoded maps
        number_map = ['', '', '', '', '', '', '', '', '', '']
        segmnt_map = ['', '', '', '', '', '', '', ]

        # capture signals using six segments, will be numbers 0, 6, & 9
        sixers = [x for x in bin_signals if x.count('1') == 6]

        #######################################
        #  determine segment map from signal  #
        #######################################

        # identify unique numbers 1, 4, 7, & 8
        # number_map[1] = [x for x in bin_signals if x.count('1') == 2][0]
        number_map[1] = get_if_count(bin_signals, 2)
        number_map[4] = get_if_count(bin_signals, 4)
        number_map[7] = get_if_count(bin_signals, 3)
        number_map[8] = get_if_count(bin_signals, 7)

        # diff 1 & 7 to determine segment a
        segmnt_map[0] = diff(number_map[1], number_map[7])

        # diff 1 & 4 to get a bin string with segments b & d
        seg_b_d = diff(number_map[1], number_map[4])

        # only one the sixers is missing segment d, invert them, bitwise and
        # with seg_b_d to find d segment, that guy is number 0
        for sixer in sixers:
            differ = andd(seg_b_d, diff(sixer, '1111111'))
            if differ.count('1'):
                segmnt_map[3] = differ
                number_map[0] = sixer
                # strip out zero so sixers is just left with 9 & 6
                sixers.remove(sixer)

        # knowing d segment we can diff with seg_b_d to find b segment
        segmnt_map[1] = diff(segmnt_map[3], seg_b_d)

        # diff the remaining sixers to get a bin string with segments c & e
        seg_c_e = orrr(diff(sixers[0], '1111111'), diff(sixers[1], '1111111'))

        # and seg_c_e with 1 to find segment c, then we also know segment e
        segmnt_map[2] = andd(seg_c_e, number_map[1])
        segmnt_map[4] = diff(segmnt_map[2], seg_c_e)

        # we can id the rest of our sixers now
        for sixer in sixers:
            # see if sixer is missing segment e, this would be 9
            differ = andd(segmnt_map[4], diff(sixer, '1111111'))
            if differ.count('1'):
                number = 9
            else:
                number = 6
            number_map[number] = sixer

        # remove all our known numbers from the signals list
        for number in number_map:
            if len(number):
                bin_signals.remove(number)

        # bin_signals now only contains numbers 2, 3, & 5
        # 3 is missing segments b and e, so build a be segment var
        # 5 is missing segments c and e, which we already know
        seg_b_e = orrr(segmnt_map[1], segmnt_map[4])

        # loop through remaining bin_signals, compare with seg_N_N to id
        for signal in bin_signals:
            if diff(seg_b_e, signal).count('1') == 7:
                number_map[3] = signal
            elif diff(seg_c_e, signal).count('1') == 7:
                number_map[5] = signal
            else:
                number_map[2] = signal

        ##################
        #  decode output #
        ##################

        # transform our number map into a dict for ease of use

        number_dict = {str(bin): str(idx) for (idx, bin) in enumerate(number_map)}

        value = ''
        for digit in bin_outputs:
            value += number_dict[digit]

        sum += int(value)

    return sum


##########
#  main  #
##########
if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
    print('Binary:', part2_binary_method())
