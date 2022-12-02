#!/usr/bin/env python3
# https://adventofcode.com/2022/day/2

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform
rounds = [tuple(line.split(" ")) for line in lines]

# A rock
# B paper
# C scissors

# X rock
# Y paper
# Z scissors

# 1 winning rock
# 2 winning paper
# 3 winning scissors

# truth table
# A  X  3  1
# A  Y  6  2
# A  Z  0  3
# B  X  0  1
# B  Y  3  2
# B  Z  6  3
# C  X  6  1
# C  Y  0  2
# C  Z  3  3
# |  |  |  |
# |  |  |  `--- played shape score
# |  |  `--- win loss draw score
# |  `--- your hand
# `--- their hand


def play_round(state: tuple) -> int:
    """
    Take what each person plays and return how many points you have earned.
    """
    us = state[1]

    shape_map = {
        'X': 1,
        'Y': 2,
        'Z': 3,
    }

    win_loss_draw_map = {
        ('A', 'X'): 3,
        ('A', 'Y'): 6,
        ('A', 'Z'): 0,
        ('B', 'X'): 0,
        ('B', 'Y'): 3,
        ('B', 'Z'): 6,
        ('C', 'X'): 6,
        ('C', 'Y'): 0,
        ('C', 'Z'): 3,
    }

    return shape_map[us] + win_loss_draw_map[state]


def play_strategy(state: tuple) -> int:
    outcome = state[1]
    if outcome == 'X':
        # need to lose
        losing = {
            'A': 'Z',
            'B': 'X',
            'C': 'Y',
        }
        play = losing[state[0]]
    elif outcome == 'Y':
        # need to draw
        draw = {
            'A': 'X',
            'B': 'Y',
            'C': 'Z',
        }
        play = draw[state[0]]
    elif outcome == 'Z':
        # need to win
        winning = {
            'A': 'Y',
            'B': 'Z',
            'C': 'X',
        }
        play = winning[state[0]]

    return play_round((state[0], play))


total = 0
for r in rounds:
    total += play_round(r)

print("part 1:", total)

total = 0
for r in rounds:
    total += play_strategy(r)

print("part 2:", total)
