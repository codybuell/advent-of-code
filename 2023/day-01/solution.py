#!/usr/bin/env python3
# https://adventofcode.com/2023/day/1

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()


def part1():
    total = 0
    for line in lines:
        nums = re.sub(r"\D", "", line)
        total += int(''.join([nums[0], nums[-1]]))
    print(total)


def part2():
    numbers = {
        # 'one':   "1",
        # 'two':   "2",
        # 'three': "3",
        # 'four':  "4",
        # 'five':  "5",
        # 'six':   "6",
        # 'seven': "7",
        # 'eight': "8",
        # 'nine':  "9",
        'one':   'on1e',
        'two':   'tw2o',
        'three': 'thr3e',
        'four':  'fo4ur',
        'five':  'fi5ve',
        'six':   'si6x',
        'seven': 'sev7en',
        'eight': 'ei8ght',
        'nine':  'ni9ne',
    }

    total = 0

    for line in lines:
        while True:
            indexes = {}

            for old, new in numbers.items():
                index = line.find(old)
                if index >= 0:
                    indexes[old] = index

            issorted = sorted(indexes.items(), key=lambda x: x[1])

            if not len(issorted):
                break

            findandrep = issorted[0][0]

            line = line.replace(findandrep, numbers[findandrep])

        nums = re.sub(r"\D", "", line)
        total += int(''.join([nums[0], nums[-1]]))

    print(total)


part1()
part2()
