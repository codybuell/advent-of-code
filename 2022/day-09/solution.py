#!/usr/bin/env python3
# https://adventofcode.com/2022/day/9

import os
import time
import curses

from curses import wrapper

################################################################################
##                                                                            ##
##  Config                                                                    ##
##                                                                            ##
################################################################################


visualize = False


################################################################################
##                                                                            ##
##  Data Prep                                                                 ##
##                                                                            ##
################################################################################


# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform into a list of list and coerce distance to an int
moves = [line.split(' ') for line in lines]
moves = [[x[0], int(x[1])] for x in moves]

# determine the size of the matrix we're working with and starting position
min_x, max_x, min_y, max_y = 0, 0, 0, 0
location = [0, 0]
for move in moves:
    if move[0] == "R":
        location[1] += move[1]
    if move[0] == "L":
        location[1] -= move[1]
    if move[0] == "U":
        location[0] += move[1]
    if move[0] == "D":
        location[0] -= move[1]

    min_x = min(min_x, location[0])
    max_x = max(max_x, location[0])
    min_y = min(min_y, location[1])
    max_y = max(max_y, location[1])

width    = abs(min_y) + max_y + 1
height   = abs(min_x) + max_x + 1
start_pos = [abs(min_x), abs(min_y)]


################################################################################
##                                                                            ##
##  Functions                                                                 ##
##                                                                            ##
################################################################################


def print_matrix(width, height, head, tail):
    stdscr.clear()

    row = ['.' for _ in range(width)]
    matrix = [row.copy() for _ in range(height)]

    # draw the matrix
    matrix.reverse()
    for idx, row in enumerate(matrix):
        # print(''.join(row))
        stdscr.addstr(idx, 0, ''.join(row), curses.color_pair(241))

    # draw our positions
    stdscr.addstr(height - start_pos[0] - 1, start_pos[1], 's', curses.color_pair(21))
    stdscr.addstr(height - tail[0] - 1, tail[1], 'T', curses.color_pair(41))
    stdscr.addstr(height - head[0] - 1, head[1], 'H', curses.color_pair(197))

    stdscr.refresh()
    time.sleep(0.08)


def print_rope(width, height, rope):
    stdscr.clear()

    row = ['.' for _ in range(width)]
    matrix = [row.copy() for _ in range(height)]

    our_rope = rope.copy()
    our_rope.reverse()

    # draw the matrix
    matrix.reverse()
    for idx, row in enumerate(matrix):
        # print(''.join(row))
        stdscr.addstr(idx, 0, ''.join(row), curses.color_pair(241))

    # draw our positions
    stdscr.addstr(height - start_pos[0] - 1, start_pos[1], 's', curses.color_pair(12))

    color_start = 246
    head = our_rope.pop()

    for node in our_rope:
        stdscr.addstr(height - node[0] - 1, node[1], '#', curses.color_pair(color_start))
        color_start += 1

    # draw the head
    stdscr.addstr(height - head[0] - 1, head[1], 'H', curses.color_pair(197))

    stdscr.refresh()
    time.sleep(0.05)


def part_1():
    loc_head = start_pos.copy()
    loc_tail = start_pos.copy()
    visited  = {
        (start_pos[0], start_pos[1]): 1,
    }

    for move in moves:
        # break out instructions
        direction = move[0]
        distance  = move[1]

        # translate direction into a vector
        if direction == 'R':
            move_head = [0, 1]
        if direction == 'L':
            move_head = [0, -1]
        if direction == 'U':
            move_head = [1, 0]
        if direction == 'D':
            move_head = [-1, 0]

        # run head movement
        for _ in range(distance):
            # calc new head tail diff and set new head loc
            loc_head = list(map(lambda a, b: a + b, loc_head, move_head))
            diff_ht  = list(map(lambda a, b: a - b, loc_head, loc_tail))

            # determine if head is adjacent to tail
            # TODO: can this be simplified by just looking at diff_ht? if any value is > 1 it's outside the shell...
            tail_shell = [[x, y] for x in range(loc_tail[0] - 1, loc_tail[0] + 2) for y in range(loc_tail[1] - 1, loc_tail[1] + 2)]
            if loc_head in tail_shell:
                if visualize:
                    print_matrix(width, height, loc_head, loc_tail)
                continue

            # move tail appropiately... if there is a diff in 2 directions we move diagonally, else only in just one direction
            to_move = [0, 0]
            if 0 in diff_ht:
                # derive move vector
                diff_idx = diff_ht.index(0) ^ 1
                diff_val = diff_ht[diff_idx]
                to_move[diff_idx] = int(diff_val / abs(diff_val))
            else:
                to_move = [int(n / abs(n)) for n in diff_ht]

            # move and track visited
            loc_tail = list(map(lambda x, y: x + y, loc_tail, to_move))
            ltt   = tuple(loc_tail)
            count = visited[ltt] if visited.get(ltt) else 0
            visited[ltt] = 1 + count

            if visualize:
                print_matrix(width, height, loc_head, loc_tail)

    return len(visited)


def part_2():
    rope = [start_pos.copy() for _ in range(10)]
    visited  = {
        (start_pos[0], start_pos[1]): 1,
    }

    for move in moves:
        # break out instructions
        direction = move[0]
        distance  = move[1]

        # translate direction into a vector
        if direction == 'R':
            move_head = [0, 1]
        if direction == 'L':
            move_head = [0, -1]
        if direction == 'U':
            move_head = [1, 0]
        if direction == 'D':
            move_head = [-1, 0]

        for _ in range(distance):
            # calc new head tail diff and set new head loc
            rope[0] = list(map(lambda a, b: a + b, rope[0], move_head))

            for i in range(1, len(rope)):
                diff_ht  = list(map(lambda a, b: a - b, rope[i - 1], rope[i]))

                # determine if head is adjacent to tail
                # TODO: can this be simplified by just looking at diff_ht? if any value is > 1 it's outside the shell...
                cur_node_shell = [[x, y] for x in range(rope[i][0] - 1, rope[i][0] + 2) for y in range(rope[i][1] - 1, rope[i][1] + 2)]
                if rope[i - 1] in cur_node_shell:
                    continue

                # move tail appropiately... if there is a diff in 2 directions we move diagonally, else only in just one direction
                to_move = [0, 0]
                if 0 in diff_ht:
                    # derive move vector
                    diff_idx = diff_ht.index(0) ^ 1
                    diff_val = diff_ht[diff_idx]
                    to_move[diff_idx] = int(diff_val / abs(diff_val))
                else:
                    to_move = [int(n / abs(n)) for n in diff_ht]

                # move segment
                rope[i] = list(map(lambda x, y: x + y, rope[i], to_move))

                # track location if end of rope
                if i == len(rope) - 1:
                    ltt   = tuple(rope[i])
                    count = visited[ltt] if visited.get(ltt) else 0
                    visited[ltt] = 1 + count

            if visualize:
                print_rope(width, height, rope)

    return len(visited)


def main(stdscr):
    return part_1(), part_2()


# init curses, config input / output, disable cursor
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

# configure use of color in curses
curses.start_color()
curses.use_default_colors()
for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)

# call program in curses wrapper to better handle failures
pt_1, pt_2 = wrapper(main)

print('part 1:', pt_1)
print('part 2:', pt_2)
