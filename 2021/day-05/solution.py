#!/usr/bin/env python
# https://adventofcode.com/2021/day/5


import re


###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform, final map grid will be 2x matrix: matrix[y][x], so parse it in a
# way that will be easy to use, also build a list of each dimension cause I'm
# too lazy to find max and min in a list of dictionaries
orthogonal_vectors = []
diagonal_vectors = []
x_dimensions = []
y_dimensions = []
pattern = re.compile("([^, ]+),([^ ]+) -> ([^, ]+),([^ ]+)")
for line in lines:
    match = re.match(pattern, line)
    x1 = int(match.group(1))
    y1 = int(match.group(2))
    x2 = int(match.group(3))
    y2 = int(match.group(4))
    x_dimensions.extend([x1, x2])
    y_dimensions.extend([y1, y2])
    # build out a list of orthogonal_vectors
    if x1 == x2 or y1 == y2:
        orthogonal_vectors.append({
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        })
    # build out a list of diagonal_vectors
    if abs(x1 - x2) == abs(y1 - y2):
        diagonal_vectors.append({
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        })

# find max x and max y so we can know the size of grid we'll need to work with
x_max = max(x_dimensions)
y_max = max(y_dimensions)

# and lastly build out a matrix of 0's
matrix = []
for y in range(y_max + 1):
    x_row = []
    for x in range(x_max + 1):
        x_row.append(0)
    matrix.append(x_row)


###########
#  funcs  #
###########


def sum_matrix():
    sum = 0
    for y in matrix:
        for x in y:
            if x >= 2:
                sum += 1
    print(sum)


###########
#  parts  #
###########


def part1():
    for path in orthogonal_vectors:
        x1 = path['x1']
        x2 = path['x2']
        y1 = path['y1']
        y2 = path['y2']
        # range through y if x is constant
        if x1 == x2:
            # determine which y is lower
            if y2 > y1:
                loop = range(y1, y2 + 1)
            else:
                loop = range(y2, y1 + 1)
            for y in loop:
                matrix[y][x1] += 1
        # else range through x
        else:
            # determine which y is lower
            if x2 > x1:
                loop = range(x1, x2 + 1)
            else:
                loop = range(x2, x1 + 1)
            for x in loop:
                matrix[y1][x] += 1

    sum_matrix()


def part2():
    # part1 already applies orthogonal_vectors to the matrix so we only need to
    # deal with diagonal vectors, note we didn't copy the matrix in part 1 so
    # it operates directly on the original list
    for path in diagonal_vectors:
        x1 = path['x1']
        x2 = path['x2']
        y1 = path['y1']
        y2 = path['y2']
        # determine if x is ascending or descending
        if x1 >= x2:
            x_dir = -1  # descending
        else:
            x_dir = 1   # ascending
        # determine if y is ascending or descending
        if y1 >= y2:
            y_dir = -1  # descending
        else:
            y_dir = 1   # ascending

        y_points = []
        for y in range(y1, y2 + y_dir, y_dir):
            y_points.append(y)
        x_points = []
        for x in range(x1, x2 + x_dir, x_dir):
            x_points.append(x)

        for i in range(len(y_points)):
            matrix[y_points[i]][x_points[i]] += 1

    sum_matrix()


##########
#  main  #
##########
if __name__ == "__main__":
    part1()
    print('---')
    part2()
