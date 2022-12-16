#!/usr/bin/env python3
# https://adventofcode.com/2022/day/15

import os
import re
import itertools

################################################################################
##                                                                            ##
##  Functions                                                                 ##
##                                                                            ##
################################################################################


def get_manhattan_distance(a: tuple, b: tuple) -> int:
    """
    Determine manhattan distance between two points in a 2d matrix.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_manhattan_coverage(center: tuple, dist: int) -> list:
    """
    Determine all coords covered by manhattan distance from provided center.
    """
    covered = []
    for i in range(dist * -1, dist + 1):
        span = dist - abs(i)
        y    = center[1] - i
        x_1  = center[0] - span
        x_2  = center[0] + span
        for x in range(x_1, x_2 + 1):
            covered.append((x, y))

    covered.reverse()

    return covered


def manhattan_coverage_ranges(center: tuple, dist: int) -> list:
    """
    Determine ranges covered by manhattan distance from provided center.
    """
    covered = {}
    for i in reversed(range(dist * -1, dist + 1)):
        span = dist - abs(i)
        y    = center[1] - i
        x_1  = center[0] - span
        x_2  = center[0] + span
        covered[y] = (x_1, x_2)
        # covered.append([(x_1, y), (x_2, y)])

    return covered


def range_diff(r1, r2):
    s1, e1 = r1
    s2, e2 = r2
    endpoints = sorted((s1, s2, e1, e2))
    result = []
    if endpoints[0] == s1 and endpoints[1] != s1:
        result.append((endpoints[0], endpoints[1]))
    if endpoints[3] == e1 and endpoints[2] != e1:
        result.append((endpoints[2], endpoints[3]))
    return result


def multirange_diff(r1_list, r2_list):
    for r2 in r2_list:
        r1_list = list(itertools.chain(*[range_diff(r1, r2) for r1 in r1_list]))
    return r1_list


################################################################################
##                                                                            ##
##  Prep Data                                                                 ##
##                                                                            ##
################################################################################

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# build dictionary of sensors and associated beacons
# sensors = {}
covered = {}
# beacons = set()
pattern = re.compile(r"^Sensor at x=([-]?\d+), y=([-]?\d+): closest beacon is at x=([-]?\d+), y=([-]?\d+)$")
for line in lines:
    # grab the coords
    match = re.match(pattern, line)
    if not match:
        print("issue matching line")
    s_x = int(match.group(1))
    s_y = int(match.group(2))
    b_x = int(match.group(3))
    b_y = int(match.group(4))

    s = (s_x, s_y)
    b = (b_x, b_y)

    # # append to beacons set
    # beacons.add(b)

    # gen metadata
    distance = get_manhattan_distance(s, b)
    coverage = manhattan_coverage_ranges(s, distance)

    # build covered dict
    for row, interval in coverage.items():
        # get known segments for the row
        known = covered.get(row)

        # if none then just add the new interval
        if known is None:
            covered[row] = [interval]
            continue

        # otherwise check for overlap with any known interval for that row merge them
        new_coverage = []
        for segment in known:
            if interval[0] <= segment[1] and interval[1] >= segment[0]:
                lowest  = min(interval[0], segment[0])
                highest = max(interval[1], segment[1])
                interval = (lowest, highest)
            else:
                new_coverage.append(segment)

        new_coverage.append(interval)
        covered[row] = new_coverage

    # # populate dictionary
    # sensors[s] = {
    #     'sensor': s,
    #     'beacon': b,
    #     'manhat': distance,
    #     'coverd': coverage,
    # }

################################################################################
##                                                                            ##
##  Part 1                                                                    ##
##                                                                            ##
################################################################################

part_1_target = 2000000

count = 0
for interval in covered[part_1_target]:
    count += interval[1] - interval[0]

print('part 1:', count)

################################################################################
##                                                                            ##
##  Part 2                                                                    ##
##                                                                            ##
################################################################################

part_2_range = 4000000

x_coord = 0
y_coord = 0
found   = False
for y in range(part_2_range + 1):
    if found:
        break

    # subtrack out each covered interval from 0 to part_2_range
    segment = (0, part_2_range)

    r1 = [segment]
    r2 = covered[y]

    diffs = multirange_diff(r1, r2)
    if len(diffs):
        for diff in diffs:
            size = diff[1] - diff[0]
            if size > 1:
                x_coord = diff[1] - 1
                y_coord = y
                found = True
                break

print('part 2:', (x_coord * 4000000) + y_coord)
