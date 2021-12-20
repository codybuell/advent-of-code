#!/usr/bin/env python
# https://adventofcode.com/2021/day/20

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
algoritm = list(lines[0])
image = [list(x) for x in lines[2:]]


###########
#  funcs  #
###########


def print_matrix(matrix: list):
    for line in matrix:
        print(''.join(line))


def pad_matrix(matrix: list, padd: int, step: int) -> list:
    """ Padd our image on all sides with dark pixels. """
    # if our algoritm starts with # our infinite pixels are going to flash to
    # our last value, else they will always stay dark... this can probably be
    # simplified as first loop will always be black and subsequent will be
    # whatever the value of algorithm 0 evaluates to and then whatever that
    # evals to etc... will always be one end of the 'algorithm'
    if algoritm[0] == '#':
        if step % 2:
            char = algoritm[0]
        else:
            char = algoritm[-1]
    else:
        char = algoritm[0]

    width      = len(matrix[0]) + (padd * 2)
    padd_top   = [list(char * width)]
    padd_side  = list(char * padd)
    new_matrix = []

    for line in matrix:
        new_matrix.append(padd_side + line + padd_side)

    return (padd_top * padd) + new_matrix + (padd_top * padd)


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
    coords_around = [list(x) for x in set(tuple(x) for x in coords_around)]
    coords_around.sort()

    # remove the coord provided
    # coords_around.remove(coord)

    return coords_around


def parse_pixel(values: list) -> str:
    values = ''.join(values)
    binary = values.replace('.', '0').replace('#', '1')
    base10 = int(binary, 2)
    return algoritm[base10]


def run_cycle(matrix: list, count: int) -> list:
    for i in range(count):
        # put in a pad
        matrix = pad_matrix(matrix, 2, i)

        # put in a placeholder to store the new image, deepcopy of matrix
        new_image = [x[:] for x in matrix]

        # loop through our image, excluding the very edge
        for idx_y in range(1, len(matrix) - 1):
            for idx_x in range(1, len(matrix[0]) - 1):
                coords_around = spaces_around([idx_y, idx_x], matrix)
                values_around = [matrix[j[0]][j[1]] for j in coords_around]
                new_image[idx_y][idx_x] = parse_pixel(values_around)

        # reset for the next loop, strip off one of the padding
        matrix = [y[1:-1] for y in new_image[1:-1]]

    return matrix


###########
#  parts  #
###########


def part1():
    # copy base image and run 50 cycles
    pt_1_image = [x[:] for x in image]
    pt_1_image = run_cycle(pt_1_image, 2)

    # count up the lit pixels
    count = 0
    for line in pt_1_image:
        count += line.count('#')

    return count


def part2():
    # copy base image and run 50 cycles
    pt_2_image = [x[:] for x in image]
    pt_2_image = run_cycle(pt_2_image, 50)

    # count up the lit pixels
    count = 0
    for line in pt_2_image:
        count += line.count('#')

    # print out final image
    print_matrix(pt_2_image)

    return count


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
