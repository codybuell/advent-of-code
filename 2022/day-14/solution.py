#!/usr/bin/env python3
# https://adventofcode.com/2022/day/14

import os
import glob
import contextlib

from PIL import Image
from copy import deepcopy

# TODO: do you need the png's as an intermediate step? just store in memory?
# TODO: optimizations on frame generation? keep prev frame and apply diff? only render sand on a base image?

################################################################################
##                                                                            ##
##  Configuration                                                             ##
##                                                                            ##
################################################################################


home_dir    = os.path.expanduser('~')
make_print  = False       # print frames to stdout
make_gif    = False       # generate a gif of the drips
frames_dir  = home_dir + "/Desktop/aoc-2022-day-14-frames"
frames_glob = home_dir + "/Desktop/aoc-2022-day-14-frames/frame_*.png"
gif_out     = home_dir + "/Desktop/aoc-2022-day-14.gif"


################################################################################
##                                                                            ##
##  Pixels                                                                    ##
##                                                                            ##
################################################################################


sand = [
    (244, 237, 219), (244, 237, 219), (205, 192, 175), (203, 190, 170), (118, 107, 90),
    (231, 217, 202), (231, 217, 202), (179, 165, 149), (155, 142, 125), (63, 49, 40),
    (212, 198, 186), (212, 198, 186), (222, 209, 197), (168, 154, 238), (100, 79, 66),
    (177, 171, 157), (177, 171, 157), (166, 156, 141), (142, 127, 112), (109, 92, 87),
    (177, 171, 157), (177, 171, 157), (166, 156, 141), (142, 127, 112), (109, 92, 87),
]

stone = [
    (98, 114, 120), (98, 114, 120), (72, 88, 94), (40, 56, 63), (40, 56, 63),
    (72, 88, 94),   (72, 88, 94),   (40, 56, 63), (72, 88, 94), (72, 88, 94),
    (72, 88, 94),   (72, 88, 94),   (40, 56, 63), (72, 88, 94), (72, 88, 94),
    (72, 88, 94),   (72, 88, 94),   (40, 56, 63), (72, 88, 94), (72, 88, 94),
    (72, 88, 94),   (72, 88, 94),   (40, 56, 63), (72, 88, 94), (72, 88, 94),
]

air = [
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
]

nozzle = [
    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),
    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),
    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),    (36, 37, 32),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
    (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228), (205, 224, 228),
]


################################################################################
##                                                                            ##
##  Functions                                                                 ##
##                                                                            ##
################################################################################


def print_matrix(matrix: list, grain: list):
    for idy, line in enumerate(matrix):
        if idy == grain[1]:
            temp = line.copy()
            temp[grain[0]] = 'o'
            print(''.join(temp))
        else:
            print(''.join(line))


def render_frame(matrix, grain):
    global frame

    # TODO: add grain to print render! it's not in the matrix

    img = Image.new('RGB', (matrix_width * 5, matrix_height * 5))
    for idy, row in enumerate(matrix):
        for idx, dot in enumerate(row):

            scale_x_ctr = (idx * 5) + 2
            scale_y_ctr = (idy * 5) + 2
            around = [[x, y] for x in range(scale_x_ctr - 2, scale_x_ctr + 3) for y in range(scale_y_ctr - 2, scale_y_ctr + 3)]

            if [idx, idy] == grain:
                pixel = sand
            elif dot == '#':
                pixel = stone
            elif dot == 'o':
                pixel = sand
            elif dot == '+':
                pixel = nozzle
            else:
                pixel = air

            for idx, loc in enumerate(around):
                img.putpixel((loc[0], loc[1]), pixel[idx])

    img.save(f'{home_dir}/Desktop/aoc-2022-day-14-frames/frame_{frame:05}.png')
    frame += 1


def render_gif():
    with contextlib.ExitStack() as stack:
        # grab images list and determine duration
        files    = glob.glob(frames_glob)
        frames   = len(files)
        fps      = 60
        duration = int(frames / fps)

        # lazy load images
        imgs = (stack.enter_context(Image.open(f)) for f in sorted(files))

        # extract  first image from iterator
        img = next(imgs)

        # build the gif
        img.save(fp=gif_out,
                 format='GIF',
                 append_images=imgs,
                 save_all=True,
                 duration=duration,
                 loop=1)


def points_between(start: list, end: list) -> list:
    min_x = min(start[0], end[0])
    max_x = max(start[0], end[0])
    min_y = min(start[1], end[1])
    max_y = max(start[1], end[1])
    if min_x == max_x:
        # x is not changing
        points = [[min_x, i] for i in range(min_y, max_y + 1)]
    else:
        # y is not changing
        points = [[i, min_y] for i in range(min_x, max_x + 1)]

    return points


def widen_matrix(matrix: list, direction: str) -> list:
    new_matrix = []

    if direction == 'left':
        # grow matrix one to the left
        for row in matrix:
            new_matrix.append(['.'])
            new_matrix[-1].extend(row)
        new_matrix[-1][0] = '#'
        return new_matrix
    elif direction == 'right':
        # grow matrix one to the right
        for row in matrix:
            new_matrix.append(row)
            new_matrix[-1].append('.')
        new_matrix[-1][-1] = '#'
        return new_matrix


def drip(matrix: list, start: list, floor: bool) -> bool:
    """
    Drip one grain of sand to a stopping point.
    """
    falling = True
    grain   = start

    global matrix_width, matrix_height

    while falling:
        if make_gif:
            # render a frame
            render_frame(matrix, grain)
        elif make_print:
            # print a frame
            print_matrix(matrix, grain)

        # grab all spaces blow the grain
        x_pos = grain[0]
        y_pos = grain[1]
        beneath_coords   = [[x_pos, i] for i in range(y_pos + 1, matrix_height)]
        beneath_material = [matrix[i][x_pos] for i in range(y_pos + 1, matrix_height)]

        # bail if there is nothing for us to land on
        if '#' not in beneath_material and 'o' not in beneath_material:
            return False, matrix

        # id location of the grain or rock directly below us
        stop_idx  = beneath_material.index(next(filter(lambda i: i != '.', beneath_material)))
        stop_loc  = beneath_coords[stop_idx - 1]

        # if we have some distance to fall go straight down
        if stop_idx > 0:
            grain = stop_loc
            continue

        # otherwise see if we can fall left
        pos_down = grain[1] + 1
        pos_left = grain[0] - 1
        if pos_left < 0 or pos_down >= matrix_height:
            if floor and pos_down < matrix_height - 1:
                matrix = widen_matrix(matrix, 'left')
                matrix_width += 1
                grain = [grain[0], pos_down]
                start[0] += 1
                continue
            elif floor:
                matrix[grain[1]][grain[0]] = 'o'
                return True, matrix
            else:
                return False, matrix
        if matrix[pos_down][pos_left] == '.':
            grain = [pos_left, pos_down]
            continue

        # otherwise see if we can fall right
        pos_right = grain[0] + 1
        if pos_right > matrix_width - 1 or pos_down >= matrix_height:
            if floor and pos_down < matrix_height - 1:
                matrix = widen_matrix(matrix, 'right')
                matrix_width += 1
                grain = [pos_right, pos_down]
                continue
            elif floor:
                matrix[grain[1]][grain[0]] = 'o'
                return True, matrix
            else:
                return False, matrix
        if matrix[pos_down][pos_right] == '.':
            grain = [pos_right, pos_down]
            continue

        # otherwise just stay put
        matrix[grain[1]][grain[0]] = 'o'

        return True, matrix


def count_grains(matrix: list) -> int:
    total = 0
    for row in matrix:
        for col in row:
            if col == 'o':
                total += 1
    return total


################################################################################
##                                                                            ##
##  Transform Data                                                            ##
##                                                                            ##
################################################################################


frame = 0

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# start position
start_pos = [500, 0]

# build coord list for each line and find min max for x y
# starting point for sand [500,0] is our current min max
vectors = []
min_x   = start_pos[0]
max_x   = start_pos[0]
min_y   = start_pos[1]
max_y   = start_pos[1]
for line in lines:
    coords = [[int(i.split(',')[0]), int(i.split(',')[1])] for i in line.split(' -> ')]
    vectors.append(coords)
    min_x = min(min_x, min(coords, key=lambda c: c[0])[0])
    max_x = max(max_x, max(coords, key=lambda c: c[0])[0])
    min_y = min(min_y, min(coords, key=lambda c: c[1])[1])
    max_y = max(max_y, max(coords, key=lambda c: c[1])[1])

# build out matrix, normalize based on range
matrix = []
for y in range(min_y, max_y + 1):
    matrix.append([])
    for x in range(min_x, max_x + 1):
        matrix[-1].append('.')

# normalize and apply start position
start_pos = [start_pos[0] - min_x, start_pos[1] - min_y]
matrix[start_pos[1]][start_pos[0]] = '+'

matrix_height = len(matrix)
matrix_width  = len(matrix[0])

# normalize all vectors and apply to matrix
for vector in vectors:
    for i in range(len(vector) - 1):
        # grab coords to compare
        point_a = vector[i]
        point_b = vector[i + 1]
        # normalize coordinates
        point_a = [point_a[0] - min_x, point_a[1] - min_y]
        point_b = [point_b[0] - min_x, point_b[1] - min_y]
        # draw points in matrix
        for rock in points_between(point_a, point_b):
            matrix[rock[1]][rock[0]] = '#'


################################################################################
##                                                                            ##
##  Part 1                                                                    ##
##                                                                            ##
################################################################################

# prep dir if needed
if make_gif:
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)


# work with a copy of the matrix
p1_matrix = deepcopy(matrix)

# simulate sand dripping
stacking  = True
while stacking:
    stacking, p1_matrix = drip(p1_matrix, start_pos, False)

print('part 1:', count_grains(p1_matrix))

if make_gif:
    render_gif()

    # clean up
    files = glob.glob(frames_glob)
    for f in files:
        os.remove(f)
    os.rmdir(frames_dir)


################################################################################
##                                                                            ##
##  Part 2                                                                    ##
##                                                                            ##
################################################################################


make_gif = False

# add the floor
matrix.append(['.' for _ in range(matrix_width)])
matrix.append(['#' for _ in range(matrix_width)])

# re-measure matrix_height
matrix_height = len(matrix)

stacking = True
while stacking:
    stacking, matrix = drip(matrix, start_pos, True)
    if '+' not in matrix[0]:
        break

print('part 2:', count_grains(matrix))
