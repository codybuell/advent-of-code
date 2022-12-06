#!/usr/bin/env python3
# https://adventofcode.com/2022/day/6

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()
line  = lines[0]


def decode(line: str, packet_size: int) -> int:
    length = len(line)
    for i in range(packet_size - 1, length):
        start = i - packet_size + 1
        chunk = set(line[start:i + 1])
        if len(chunk) == packet_size:
            return i + 1


print('part 1:', decode(line, 4))
print('part 2:', decode(line, 14))
