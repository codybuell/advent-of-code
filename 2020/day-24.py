#!/usr/bin/env python3
# https://adventofcode.com/2020/day/24

import re
import sys
import copy

dataFile         = open('day-24.txt', 'r')
instructions_raw = dataFile.read().splitlines()

def parse_instructions():
    # build a movements dictionary (y,x)
    movement = {
            'ne': (-1, 0),
            'e' : (0, 1),
            'se': (1, 1),
            'sw': (1, 0),
            'w' : (0, -1),
            'nw': (-1, -1)
            }

    # build a list of tuples for each instruction set
    instructions = []
    for instruction in instructions_raw:
        instruction_set = []
        while instruction:
            for motion in movement:
                m = re.match('^' + motion, instruction)
                if m:
                    instruction = instruction.replace(m.group(), '', 1)
                    instruction_set.append(movement[m.group()])

        instructions.append(instruction_set)

    return instructions

def get_board_size(instructions):

    # determine the extremes of navigation for each instruction set
    max_ys, max_xs = [], []
    for instruction_set in instructions:
        # build an arrays of every visited y and x location
        y_locs, x_locs = [], []
        y_pos, x_pos = 0, 0
        for y, x in instruction_set:
            y_pos += y
            x_pos += x
            # append absolute value as we don't care which direction
            y_locs.append(abs(y_pos))
            x_locs.append(abs(x_pos))
        # add the extreme of where we visited
        max_ys.append(max(y_locs))
        max_xs.append(max(x_locs))

    # figure out width and height, furthest visited y or x across all intsruction sets
    # plus odd value so that we have an odd number of y and x, giving us a center tile
    # making the board large enough so we dont have to deal with floor growth in part2
    height = (max(max_ys) * 2) + 201
    width  = (max(max_xs) * 2) + 201

    return height, width

def part1():
    # get our instructions and board size
    instructions  = parse_instructions()
    height, width = get_board_size(instructions)
    board_center  = (height//2, width//2)

    # make our floor, [y][x] matrix of hex centroids, set values to white (1)
    floor = []
    for y in range(height):
        floor.append([])
        for _ in range(width):
            floor[y].append(1)

    for instructions_set in instructions:
        # run our movements
        loc = list(board_center)
        for motion in instructions_set:
            loc[0] += motion[0]
            loc[1] += motion[1]
        # flip the tile
        floor[loc[0]][loc[1]] ^= 1

    # count black tiles
    count = 0
    for y in floor:
        count += y.count(0)

    print(count)

    return floor

def part2(floor):
    # define motions to tiles aruond any given tile
    around = [(-1, 0), (0, 1), (1, 1), (1, 0), (0, -1), (-1, -1)]

    # get dimensions so we dont' check outer border
    y_size = len(floor)
    x_size = len(floor[0])
    # iterate through 100 days
    for d in range(100):

        floor_next = copy.deepcopy(floor)
        for idxy, y in enumerate(floor):
            # skip our borders
            if idxy <= 1 or idxy >= y_size - 1:
                continue
            for idxx, x in enumerate(y):
                # skip our borders
                if idxx <= 1 or idxx >= x_size - 1:
                    continue

                # build list of locations around current tile
                locations_around = []
                for ay, ax in around:
                    locations_around.append((idxy + ay, idxx + ax))

                # build a list of values around
                values_around = []
                for ay, ax in locations_around:
                    values_around.append(floor[ay][ax])

                # count up black tiles
                blacks = values_around.count(0)

                # if tile is black with zero or more than two blacks adjacent 
                # or if tile is white with exactly 2 blacks adjacent, FLIP
                if (x == 0 and (blacks == 0 or blacks > 2)) or (x == 1 and blacks == 2):
                    floor_next[idxy][idxx] ^= 1

        # apply changes simultaneously
        floor = floor_next

        count = 0
        for y in floor:
            count += y.count(0)
        print('Day', d + 1, ':', count)

if __name__ == "__main__":
    floor = part1()
    part2(floor)
