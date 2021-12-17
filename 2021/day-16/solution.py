#!/usr/bin/env python
# https://adventofcode.com/2021/day/16

###########
#  setup  #
###########


verbose = False


# ingest data
dataFile = open('data.txt', 'r')
hexadecimal = dataFile.read().rstrip()

# set up a map
hex_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

# transform hex to 4 bit binary
binary_string = ''
for hex in list(hexadecimal):
    binary_string += (hex_map[hex])


###########
#  funcs  #
###########


def read_packet_header(bin: str) -> list:
    packet_version_bin = bin[:3]
    packet_type_id_bin = bin[3:6]

    packet_version = int(packet_version_bin, 2)
    packet_type_id = int(packet_type_id_bin, 2)

    return packet_version, packet_type_id, bin[6:]


def parse_literal_value(bin: str) -> list:
    # literal value packet type, groups of 4 bits padded w/leading 0's until
    # len is 4, each group prefixed by 1 except the last which is 0 prefixed
    number = ''
    while True:
        firstbit = bin[0]
        number  += bin[1:5]
        bin      = bin[5:]

        # print(firstbit, number, bin)

        # if first bit is zero, is last group, break
        if firstbit == '0':
            break

    number = int(number, 2)

    return number, bin


def process(bin: str, sum: int, indent: int, values: list) -> list:
    # set some padding for our prints to help readability
    padding = " " * indent

    # get our packet header and add in our version
    version, type_id, bin = read_packet_header(bin)
    sum += version

    # operate based on type of packet
    if type_id == 4:
        # literal value packet, get it's value and move on
        number, bin = parse_literal_value(bin)
        values.append(number)

        if verbose:
            print(padding, '### literal value packet ###')
            print(padding, 'ver:', version)
            print(padding, 'val: ', number)

    else:
        # we're dealing with an operator packet of some type
        length_type_id = bin[0]
        subvalues = []

        if verbose:
            print(padding, '***** operator packet *****')
            print(padding, 'ver:', version)

        if length_type_id == '0':
            if verbose:
                print(padding, '  type: 0')
            # next 15 bits are a number that represents the total length in
            # bots of the subpackets contained by this packet
            bit_length_bin = bin[1:16]
            bit_length = int(bit_length_bin, 2)
            all_subpackets_bin = bin[16:16 + bit_length]
            if verbose:
                print(padding, '  VV processing', bit_length, 'bits of subpackets VV')
            subvalues = []
            while True:
                if len(all_subpackets_bin) and int(all_subpackets_bin, 2) != 0:
                    all_subpackets_bin, sum, subvalues = process(all_subpackets_bin, sum, indent + 2, subvalues)
                else:
                    break
            bin = bin[16 + bit_length:]
        else:
            if verbose:
                print(padding, 'op pac type: 1')
            # next 11 bits are a number that represents the number of
            # sub-packets immediately contained by this packet
            sub_packets_count_bin = bin[1:12]
            sub_packets_count = int(sub_packets_count_bin, 2)
            bin = bin[12:]
            # process the indicated number of sub_packets
            if verbose:
                print(padding, '  VV processing', sub_packets_count, 'subpackets VV')
            subvalues = []
            for i in range(sub_packets_count):
                bin, sum, subvalues = process(bin, sum, indent + 2, subvalues)

        to_append = process_sub_values(type_id, subvalues)
        values.append(to_append)

    return bin, sum, values


def process_sub_values(type_id: int, subvalues: list) -> int:
    if type_id == 0:
        subsum = 0
        for v in subvalues:
            subsum += v
        return subsum
    if type_id == 1:
        subprod = 1
        for v in subvalues:
            subprod *= v
        return subprod
    if type_id == 2:
        return min(subvalues)
    if type_id == 3:
        return max(subvalues)
    if type_id == 5:
        firstsub = subvalues[0]
        seconsub = subvalues[1]
        if firstsub > seconsub:
            return 1
        else:
            return 0
    if type_id == 6:
        firstsub = subvalues[0]
        seconsub = subvalues[1]
        if firstsub < seconsub:
            return 1
        else:
            return 0
    if type_id == 7:
        firstsub = subvalues[0]
        seconsub = subvalues[1]
        if firstsub == seconsub:
            return 1
        else:
            return 0


###########
#  parts  #
###########


def part1():
    bin = binary_string
    sum = 0
    values = []

    # process packets until we're done
    while True:
        if len(bin) and int(bin, 2) != 0:
            bin, sum, values = process(bin, sum, 0, values)
        break

    return sum


def part2():
    bin = binary_string
    sum = 0
    values = []

    # process packets until we're done
    while True:
        if len(bin) and int(bin, 2) != 0:
            bin, sum, values = process(bin, sum, 0, values)
        break

    tot_val = 0
    for val in values:
        tot_val += val
    return tot_val


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
