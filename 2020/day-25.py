#!/usr/bin/env python3
# https://adventofcode.com/2020/day/25

import re
import sys

dataFile = open('day-25.txt', 'r')
pubkeys  = dataFile.read().splitlines()

def get_loop_size(subj_number, key):
    value        = 1
    loop_size    = 1
    while True:
        value *= subj_number
        value %= 20201227
        if value == key:
            return loop_size
        loop_size += 1

def part1():
    card_pub_key = int(pubkeys[0])
    door_pub_key = int(pubkeys[1])
    subject_numb = 7

    # determine the card loop size
    cls = get_loop_size(subject_numb, card_pub_key)

    # transorm on card
    subj_number = door_pub_key
    value       = 1
    for i in range(cls):
        value *= subj_number
        value %= 20201227

    print('card encryption key:', value)

def part2():
    pass

if __name__ == "__main__":
    part1()
    part2()
