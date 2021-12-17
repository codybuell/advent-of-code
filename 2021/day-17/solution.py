#!/usr/bin/env python
# https://adventofcode.com/2021/day/17

import re

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
line = dataFile.read().rstrip()

# transform
p = re.compile(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)")
m = re.match(p, line)
x1 = int(m.group(1))
x2 = int(m.group(2))
y1 = int(m.group(3))
y2 = int(m.group(4))

# # build a list of coords that constitute the trench
# x_range = [x for x in range(x1, x2 + 1)]
# y_range = [y for y in range(y1, y2 + 1)]
# y_range.reverse()
# target_coords = []
# for x in x_range:
#     for y in y_range:
#         target_coords.append([x, y])


###########
#  funcs  #
###########


def step(velocity: list, position: list) -> list:
    """ returns two lists, new velocity and new position """
    new_pos = [position[0] + velocity[0], position[1] + velocity[1]]

    x_vel = velocity[0]
    y_vel = velocity[1]

    # move x velocity towards 0
    if x_vel > 0:
        x_vel = x_vel - 1
    elif x_vel < 0:
        x_vel = x_vel + 1

    new_vel = [x_vel, y_vel - 1]

    return new_vel, new_pos


def run_velocities(velocities: list) -> dict:
    """ build a dict of successful initial velocities and their corresponoding
    max y positions """
    # start a dict of successful trajectories with their y maxes
    successful = {}

    # loop through velocities
    for velocity in velocities:

        # start a var of y max = 0
        y_max = 0

        # note the starting velocity
        starting_velocity = str(velocity[0]) + "," + str(velocity[1])

        # init our starting position
        position = [0, 0]

        # print(position)

        # while true
        while True:
            # run a step
            velocity, position = step(velocity, position)
            # print(position)

            # so we don't have to write so much
            x = position[0]
            y = position[1]

            # if y position > y max set it as new y max
            if y > y_max:
                y_max = y

            # check new position, if right of x2 or below y2 break, we didn't make it
            if x > x2 or y < y1:
                # print('overshot :(')
                break

            # if >= x1 and <= x2 and <= y1 and >= y2 break, we're in the trench
            if x >= x1 and x <= x2 and y <= y2 and y >= y1:
                # print('nailed it :)')
                # append ymax and starting velocity to successful dict
                successful[starting_velocity] = y_max
                break

    return successful


###########
#  parts  #
###########


def part1():
    # build a list of coords that constitute the trench
    x_range = [x for x in range(0, x2 + 2)]     # we can't have a x vel higher than right side of trench
    y_range = [y for y in range(y1, 200)]       # TODO: figure out some logic here...
    velocities = []
    for x in x_range:
        for y in y_range:
            velocities.append([x, y])

    successful = run_velocities(velocities)

    # now get the successful entry with the highest y_max
    ymx_small_to_big = [v for k, v in sorted(successful.items(), key=lambda item: item[1])]
    # vel_small_to_big = [k for k, v in sorted(successful.items(), key=lambda item: item[1])]

    return(ymx_small_to_big[-1])


def part2():
    # build a list of coords that constitute the trench
    x_range = [x for x in range(0, x2 + 2)]     # we can't have a x vel higher than right side of trench
    y_range = [y for y in range(y1, 800)]       # TODO: figure out some logic here...
    velocities = []
    for x in x_range:
        for y in y_range:
            velocities.append([x, y])

    successful = run_velocities(velocities)

    return(len(successful))


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
