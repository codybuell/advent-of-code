#!/usr/bin/env python3
# https://adventofcode.com/2020/day/23

import sys

dataFile = open('day-23.txt', 'r')
sequence = [int(x) for x in dataFile.read().rstrip()]

def rearrange(sequence, index):
    new_seq = sequence[index + 1:]
    new_seq.extend(sequence[:index + 1])
    return new_seq

def crab_cups(seq, iterations, part):
    # establish some metadata about our sequence
    cmin = min(seq)                               # id the lowest value cup
    cmax = max(seq)                               # id the highest value cup
    slen = len(seq)                               # length of the sequence

    # rearrange our sequence so the current cup is seq[-1]
    seq  = rearrange(seq, 0)

    # run 100 interations of the game
    for i in range(iterations):
        # pick up the three cups after the current cup (seq[0:3])
        picked = seq[0:3]
        seq    = seq[3:]

        # print('-- move', i + 1, '--')
        # print('cups:', seq, '<-- current cup')
        # print('pick up:', picked)

        # note the curren cup value

        cc_val = seq[-1]

        # determine the destination cup
        dest_val = cc_val - 1
        while True:
            # if we've dropped off the low end, loop back to the max value
            if dest_val < cmin:
                dest_val = cmax

            # if new destination is in sequence (not picked up) get it's index
            if dest_val in seq:
                dest_idx = seq.index(dest_val)
                break

            # otherwise go down by one and loop
            dest_val -= 1

        # print('destination:', dest_val)

        # place picked up cups right after the destination cup
        seq[dest_idx + 1:dest_idx + 1] = picked

        # get the index of the next 'current cup'
        next_cc_idx = (seq.index(cc_val) + 1) % slen

        # rearrange to put next current cup at the back of the list
        seq = rearrange(seq, next_cc_idx)

    # get index of 1
    one_idx = seq.index(1)

    # re-arrange to put it on the back
    seq = rearrange(seq, one_idx)

    if part == 1:
        # final number list is seq following 1
        seq.pop()
        final_seq = [str(x) for x in seq]
        print(''.join(final_seq))
    elif part == 2:
        # final number is product of two cups after cup 1
        prod = seq[0] * seq[1]
        print(prod)

def crab_cups_mkii(seq, iterations, part):
    # establish some metadata about our sequence
    cmin = min(seq)
    cmax = max(seq)
    clen = len(seq)

    # make a faux linked list using a dictionary
    # key returns the val of the next clockwise cup, the last
    # cup in the loop points to the first cup making our loop
    cup_seq_lookup = {c1: c2 for c1, c2 in zip(seq, seq[1:] + [seq[0]])}

    # grab our initial current cup
    current_cup = seq[0]

    # run our iterations
    for i in range(iterations):

        # 'pick up' the next three cups
        x = current_cup
        picked = [x := cup_seq_lookup[x] for _ in range(3)]

        # calculate our destination cup
        destination = current_cup - 1
        while destination <= 0 or destination in picked:
            destination -= 1
            if destination <= 0:
                destination = cmax

        # rearrange our cups
        # the current cup will point to something new (whatever the last cup we picked up pointed to)
        # the last cup in our picked up seq will point to someting new (cup after dest)
        # the destination cup will point to something new (first cup in picked seq)
        cup_seq_lookup[current_cup] = cup_seq_lookup[picked[-1]]
        cup_seq_lookup[picked[-1]]  = cup_seq_lookup[destination]
        cup_seq_lookup[destination] = picked[0]

        # determine the next 'current cup', will be to the right of current cup
        current_cup = cup_seq_lookup[current_cup]

    if part == 1:
        # final number list is seq following 1
        x = 1
        final_seq = [x := cup_seq_lookup[x] for _ in range(clen - 1)]
        print(''.join([str(x) for x in final_seq]))
    elif part == 2:
        # final number is product of two cups after cup 1
        after_1  = cup_seq_lookup[1]
        and_then = cup_seq_lookup[after_1]
        prod = after_1 * and_then
        print(prod)

def part1():
    # run 100 cycles of the game the game
    crab_cups_mkii(sequence, 100, 1)

def part2():
    # make 10 million cups (append as needded onto starting cups)
    maximum = max(sequence)
    for v in range(maximum + 1, 1000001):
        sequence.append(v)

    # run 10 million cycles of the game
    crab_cups_mkii(sequence, 10000000, 2)

if __name__ == "__main__":
    part1()
    part2()
