#!/usr/bin/env python3
# https://adventofcode.com/2022/day/8

import os

# ingest data
data = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')

# translate into a 2d matrix then copy and rotate it for easier column handling
rows = [[int(x) for x in line] for line in data.read().splitlines()]
cols = [list(row) for row in list(zip(*rows))]


################################################################################
##                                                                            ##
##  Overdone, overcomplicated first pass looking in on the forest...          ##
##                                                                            ##
################################################################################


visible = set()
row_end = len(rows) - 1
col_end = len(cols) - 1

# view from left and right
for idx, row in enumerate(rows):
    # viewing row from the left
    height = 0
    for idy, tree in enumerate(row):
        # handle top and bottom row
        if idx == 0 or idx == row_end:
            visible.add((idx, idy))
            continue
        # handle left edge
        if idy == 0:
            visible.add((idx, idy))
            height = tree
            continue
        # the middle bits
        if tree > height:
            visible.add((idx, idy))
            height = tree
            continue
        # the right edge
        if idy == col_end:
            visible.add((idx, idy))

    # viewing row from the right
    height = 0
    reversed_row = row[::-1]
    for idy, tree in enumerate(reversed_row):
        # handle top and bottom row
        if idx == 0 or idx == row_end:
            continue
        # handle right edge
        if idy == 0:
            height = tree
            continue
        # handle middle bits
        if tree > height:
            visible.add((idx, col_end - idy))
            height = tree
            continue
        # handle left edge
        if idy == col_end:
            continue

# view from top and bottom
for idy, col in enumerate(cols):
    # from the top
    height = 0
    for idx, tree in enumerate(col):
        # handle left and right column
        if idy == 0 or idy == col_end:
            visible.add((idx, idy))
            continue
        # handle top edge
        if idx == 0:
            visible.add((idx, idy))
            height = tree
            continue
        # handle the middle bits
        if tree > height:
            visible.add((idx, idy))
            height = tree
            continue
        # handle the bottom edge
        if idx == col_end:
            visible.add((idx, idy))

    # from the bottom
    height = 0
    reversed_col = col[::-1]
    for idx, tree in enumerate(reversed_col):
        # handle left and right column
        if idy == 0 or idy == col_end:
            continue
        # handle the bottom edge
        if idx == 0:
            height = tree
            continue
        # handle the middle bits
        if tree > height:
            visible.add((row_end - idx, idy))
            height = tree
            continue
        # handle the top edge
        if idx == row_end:
            continue

print('part 1a:', len(visible))


################################################################################
##                                                                            ##
##  Part 2, with a reworking of an over-engineered part 1...                  ##
##                                                                            ##
################################################################################


def score_view(direction: list, tree_fort: int) -> int:
    score = 0
    for tree in direction:
        score += 1
        if tree >= tree_fort:
            break
    return score


scores = []
visibles = 0

# loop through every tree
for idx, row in enumerate(rows):
    for idy, tree_fort in enumerate(row):

        # gather our views
        view_north = cols[idy][:idx]
        view_east  = row[idy + 1:]
        view_south = cols[idy][idx + 1:]
        view_west  = row[:idy]

        # flip north and west so it's as seen from the tree
        view_north.reverse()
        view_west.reverse()

        # determine if the tree is visible in any direction
        if (not view_north
                or not view_east
                or not view_south
                or not view_west
                or tree_fort > max(view_north)
                or tree_fort > max(view_east)
                or tree_fort > max(view_south)
                or tree_fort > max(view_west)):
            visibles += 1

        # derive our score for each direction
        north_score = score_view(view_north, tree_fort)
        east_score  = score_view(view_east, tree_fort)
        south_score  = score_view(view_south, tree_fort)
        west_score  = score_view(view_west, tree_fort)

        # derive total score and append to our list
        scores.append(north_score * east_score * south_score * west_score)

print('part 1b:', visibles)
print('part 2:', max(scores))
