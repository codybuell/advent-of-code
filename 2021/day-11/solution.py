#!/usr/bin/env python
# https://adventofcode.com/2021/day/11


import time
import curses


###########
#  setup  #
###########


# use curses or not
run_curses = True

# ingest data and convert to matrix of ints
dataFile = open('data.txt', 'r')
data = [list(map(int, x)) for x in dataFile.read().splitlines()]


###########
#  funcs  #
###########


def spaces_around(coord: list, matrix: list) -> list:
    """ Provides all spaces around a provided coordinate, constrained by the
    edges of the 2 dimensional matrix. """

    # set some ranges for edge detection
    y_range = len(matrix) - 1
    x_range = len(matrix[0]) - 1

    # define how far out from coord we want to check
    check_range = range(-1, 2)

    # build a list of all locations around coordinate, account for edge limits on y and x dimensions
    coords_around = [[min(y_range, max(0, coord[0] + y)), min(x_range, max(0, coord[1] + x))] for y in check_range for x in check_range]

    # sort and deduplicate them
    coords_around.sort()
    coords_around = [list(x) for x in set(tuple(x) for x in coords_around)]

    # remove the coord provided
    coords_around.remove(coord)

    return coords_around


def run_flashes(matrix: list, flashed: list, flashes: int) -> list:
    flashes = 0
    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            loc = [y, x]
            around = spaces_around(loc, data)
            # values = [data[j[0]][j[1]] for j in around]

            # if the location we are checking is greater than 9 flash
            if val > 9:
                flashed.append(loc)
                flashes += 1
                for octopus in around:
                    if octopus not in flashed:
                        matrix[octopus[0]][octopus[1]] += 1
                matrix[y][x] = 0
    return flashes


def print_matrix(matrix: list):
    for line in matrix:
        print(line)
    print('----')


def compare_matrices(a: list, b: list) -> bool:
    """ Compares two dimensional matrices and returns True if they are
    identical. """
    for y in range(len(a)):
        for x in range(len(a[0])):
            if a[y][x] != b[y][x]:
                return False
    return True


def print_matrix_curses(matrix: list, cycle: int):
    # nuclear option to make sure there are no artifacts from previous frame
    # may not be necessary if you are sure you are overwritting every coord
    # stdscr.clear()

    # map out our data to the screen
    for y, line in enumerate(matrix):
        for x, val in enumerate(line):
            stdscr.addstr(1, 2, "cycle " + str(cycle) + ":")
            if val == 0:
                lvl = curses.A_BOLD + curses.color_pair(10)
            else:
                lvl = curses.A_DIM + curses.color_pair(val)

            stdscr.addstr(y + 2, (x + 1) * 2, str(val), lvl)

    # draw it
    stdscr.refresh()

    # slow it down if needed
    time.sleep(1 / 20)


###########
#  parts  #
###########


def part1(cycles: int):
    flash_count = 0
    matrix = [x[:] for x in data]

    # print_matrix(matrix)
    if run_curses:
        print_matrix_curses(matrix, 0)

    for i in range(cycles):
        # track who has flashed
        flashed_coords = []

        # increase all energy levels by 1
        matrix = [[x + 1 for x in y] for y in matrix]

        # run initial flashes
        while True:
            # need to do a deep copy else we won't be getting anything different
            loop_start = [x[:] for x in matrix]
            flash_count += run_flashes(matrix, flashed_coords, flash_count)

            if compare_matrices(loop_start, matrix):
                break

        # print_matrix(matrix)
        if run_curses:
            print_matrix_curses(matrix, i)

    return flash_count


def part2():
    cycle = 0
    flash_count = 0
    matrix = [x[:] for x in data]
    # print_matrix(matrix)
    if run_curses:
        print_matrix_curses(matrix, 0)

    while True:

        # track how many cycles we've gone through and who has flashed
        cycle += 1
        flashed_coords = []

        # increase all energy levels by 1
        matrix = [[x + 1 for x in y] for y in matrix]

        # run initial flashes
        while True:
            # need to do a deep copy else we won't be getting anything different
            loop_start = [x[:] for x in matrix]
            flash_count += run_flashes(matrix, flashed_coords, flash_count)

            if compare_matrices(loop_start, matrix):
                break

        # print_matrix(matrix)
        if run_curses:
            print_matrix_curses(matrix, cycle)

        sum = 0
        for y in matrix:
            for x in y:
                sum += x
        if sum == 0:
            return cycle


##########
#  main  #
##########


if __name__ == "__main__":
    if run_curses:
        # standard curses init
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        # setup for color, auto define some color pairs
        curses.start_color()
        curses.use_default_colors()
        # map color pair number to potential octopus value, -1 is no background
        curses.init_pair(1, 237, -1)    # -
        curses.init_pair(2, 238, -1)    # --
        curses.init_pair(3, 239, -1)    # ---
        curses.init_pair(4, 240, -1)    # ----
        curses.init_pair(5, 241, -1)    # -----
        curses.init_pair(6, 242, -1)    # ------
        curses.init_pair(7, 243, -1)    # -------
        curses.init_pair(8, 244, -1)    # --------
        curses.init_pair(9, 245, -1)    # ---------
        curses.init_pair(10, 21, -1)    # ** flashed **

        # run our parts
        try:
            pt_1 = part1(100)
            pt_2 = part2()
        # return the terminal to normal
        finally:
            curses.echo()
            curses.nocbreak()
            curses.endwin()

        # print final answers
        print('Part 1:', pt_1)
        print('Part 2:', pt_2)

    else:
        print('Part 1:', part1(100))
        print('Part 2:', part2())
