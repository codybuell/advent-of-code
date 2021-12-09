#!/usr/bin/env python
# https://adventofcode.com/2021/day/9


import itertools


###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform into a 2 dimensional matrix data[y][x]
data = [list(x) for x in lines]

# capture low points here because we're lazy
low_points = []


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
    coords_around = [coords_around for coords_around, _ in itertools.groupby(coords_around)]

    # in case we dont want to return the provided coordinate in the list
    # coords_around.remove(coord)

    return coords_around


def spaces_orthogonal(coord: list, matrix: list) -> list:
    """ Provides all orthogonal spaces around a provided coordinate,
    constrained by the edges of the 2 dmensional matrix. """

    # set some ranges for edge detection
    y_range = len(matrix) - 1
    x_range = len(matrix[0]) - 1

    # define how far out from coord we want to check
    check_range = range(-1, 2)

    # grab rough list of orthogonal coordinates
    orthog_coords = []
    for y_offset in check_range:
        orthog_coords.append([min(y_range, max(0, coord[0] + y_offset)), coord[1]])
    for x_offset in check_range:
        orthog_coords.append([coord[0], min(x_range, max(0, coord[1] + x_offset))])

    # sort and deduplicate them
    orthog_coords.sort()
    orthog_coords = [orthog_coords for orthog_coords, _ in itertools.groupby(orthog_coords)]

    # in case we dont want to return the provided coordinate in the list
    # orthog_coords.remove(coord)

    return orthog_coords


def get_low_points():
    checked_locs = []
    for idx_y, y in enumerate(data):
        for idx_x, x in enumerate(y):
            # define our coordinate, get orthogonal spaces around and their
            # corresponding values
            coord = [idx_y, idx_x]
            around = spaces_orthogonal(coord, data)
            values = [data[s[0]][s[1]] for s in around]

            # print("coordinate:", coord)
            # print("loc around:", around)
            # print("val around:", values)

            # determine the min value and all associated indexes
            min_value = min(values)
            min_index = [idx for idx, v in enumerate(values) if v == min_value]

            # separate out min value indices from non min value indices
            non_min_locs = []
            min_locs = []
            for idx, loc in enumerate(around):
                if idx in min_index:
                    min_locs.append(loc)
                else:
                    non_min_locs.append(loc)

            # print("non min locs:", non_min_locs)
            # print("minimum locs:", min_locs)

            # remove non min values coords if present in low_points list
            for loc in non_min_locs:
                if loc in low_points:
                    low_points.remove(loc)

            # remove visited locations from min_locs, eles add to low points
            for loc in min_locs:
                if loc in checked_locs:
                    continue
                elif loc not in low_points:
                    low_points.append(loc)

            # add all checked locs to checked_locs
            for loc in around:
                if loc not in checked_locs:
                    checked_locs.append(loc)

            # print("low_points:", low_points)


def crawl_location(coord: list, part_of: list) -> list:
    # get value of current location
    target = int(data[coord[0]][coord[1]])

    # print("coordinate:", coord)
    # print("coord val: ", target)

    # get surrounding coordinates and corresponding values, note that it
    # contains coord and its value
    around = spaces_orthogonal(coord, data)
    values = [int(data[s[0]][s[1]]) for s in around]

    # print("loc around:", around)
    # print("val around:", values)

    # gather all locations that are a part of the basin
    for idx, value in enumerate(values):
        if value >= target and value < 9:
            if around[idx] not in part_of:
                part_of.append(around[idx])
                # print(value, around[idx])
                crawl_location(around[idx], part_of)

    return part_of


###########
#  parts  #
###########


def part1():
    # grab low points
    get_low_points()

    # sum up all their values
    sum = 0
    for loc in low_points:
        sum += 1 + int(data[loc[0]][loc[1]])

    return sum


def part2():

    # crawl all low points to determine basin sizes
    basin_sizes = []
    for loc in low_points:
        basin = crawl_location(loc, [])
        basin_sizes.append(len(basin))

    # sort to determine our largest 3
    basin_sizes.sort()

    # multiply 3 largest basins together
    factor = 1
    for i in basin_sizes[-3:]:
        factor *= i

    return factor


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
