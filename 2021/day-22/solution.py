#!/usr/bin/env python
# https://adventofcode.com/2021/day/22

import re

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
instructions = []
p = re.compile(r"(^[^\s]+)\sx=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$")
for line in lines:
    m = re.match(p, line)
    instructions.append({
        'action':  m.group(1),
        'x_start': int(m.group(2)),
        'x_stop':  int(m.group(3)),
        'y_start': int(m.group(4)),
        'y_stop':  int(m.group(5)),
        'z_start': int(m.group(6)),
        'z_stop':  int(m.group(7)),
    })


###########
#  class  #
###########


class Cuboid():
    z_start = None
    z_stop  = None
    y_start = None
    y_stop  = None
    x_start = None
    x_stop  = None
    volume  = 0
    action  = None

    def __init__(self, cuboid: dict):
        # pull in the provided info
        self.action  = cuboid['action']
        self.z_start = cuboid['z_start']
        self.z_stop  = cuboid['z_stop']
        self.y_start = cuboid['y_start']
        self.y_stop  = cuboid['y_stop']
        self.x_start = cuboid['x_start']
        self.x_stop  = cuboid['x_stop']

        # derive some of our own if not provided
        if 'volume' in cuboid:
            self.volume = cuboid['volume']
        else:
            self.set_volume()

    def turn_off(self):
        """ Set the action attribute to off. """
        self.action = 'off'

    def set_volume(self):
        """ Set the volume attribute of cuboid based on current definition. """
        # determine the width of cuboid in each dimension
        z = abs(self.z_stop - self.z_start + 1)
        y = abs(self.y_stop - self.y_start + 1)
        x = abs(self.x_stop - self.x_start + 1)

        # set the volume
        self.volume = z * y * x

    def positions(self):
        """ Calculate and return the coordinates for every cube in cuboid. """
        positions = []
        for z in range(self.z_start, self.z_stop + 1):
            for y in range(self.y_start, self.y_stop + 1):
                for x in range(self.x_start, self.x_stop + 1):
                    positions.append((z, y, x))

        return positions

    def overlap(self, cuboid: object) -> list:
        """ Calculate and return a cuboid that represents the overlap of this
        and the provided cuboid. """
        # determine if there is overlap in each of the coords, 0 if none else size
        overlap_z = max(min(self.z_stop, cuboid.z_stop) - max(self.z_start, cuboid.z_start) + 1, 0)
        overlap_y = max(min(self.y_stop, cuboid.y_stop) - max(self.y_start, cuboid.y_start) + 1, 0)
        overlap_x = max(min(self.x_stop, cuboid.x_stop) - max(self.x_start, cuboid.x_start) + 1, 0)

        # determine the overlap volume
        overlap_vol = overlap_z * overlap_y * overlap_x

        # TODO: if trying to implement method where we would need remains of an overlap
        # remainder = self.remainder(cuboid, [overlap_z, overlap_y, overlap_x])

        # determine if the resulting overlap should be on or off
        if self.action == cuboid.action:
            # if both source cuboids, toggle the self cuboid
            overlap_action = 'on' if self.action == 'off' else 'off'
        elif self.action == 'on' and cuboid.action == 'off':
            # if self is on and provided cuboid off, then sit it as on
            overlap_action = 'on'
        else:
            # else set it as off...
            overlap_action = 'off'

        cuboid = Cuboid({
            # 'action':  'off' if overlap_action == -1 else 'on',
            'action':  overlap_action,
            'volume':  overlap_vol,
            'z_start': max(self.z_start, cuboid.z_start),
            'z_stop':  min(self.z_stop, cuboid.z_stop),
            'y_start': max(self.y_start, cuboid.y_start),
            'y_stop':  min(self.y_stop, cuboid.y_stop),
            'x_start': max(self.x_start, cuboid.x_start),
            'x_stop':  min(self.x_stop, cuboid.x_stop),
        })

        # return cuboid, remainder
        return cuboid

    def intersects(self, cuboid: object) -> bool:
        """ Determine if the provided cuboid intersects with the this cuboid. """
        # determine if there is overlap in each of the coords, 0 if none else size
        if not(max(min(self.z_stop, cuboid.z_stop) - max(self.z_start, cuboid.z_start) + 1, 0)):
            return False

        if not(max(min(self.y_stop, cuboid.y_stop) - max(self.y_start, cuboid.y_start) + 1, 0)):
            return False

        if not(max(min(self.x_stop, cuboid.x_stop) - max(self.x_start, cuboid.x_start) + 1, 0)):
            return False

        return True

    def remainder(self, cuboid: object, overlaps: list) -> list:
        """ Provide cuboid remainders of each source cuboid when running an intersection. """
        # TODO: this needs to be implemented the rest of the way...
        # coordinate remainders for cuboid self
        remainder_sefl_z = cuboid.z_stop - cuboid.z_start + 1 - overlaps[0]
        remainder_sefl_y = cuboid.y_stop - cuboid.y_start + 1 - overlaps[1]
        remainder_sefl_x = cuboid.x_stop - cuboid.x_start + 1 - overlaps[2]

        # coordinate remainders for cuboid provided cuboid
        remainder_cuboid_z = self.z_stop - self.z_start + 1 - overlaps[0]
        remainder_cuboid_y = self.y_stop - sefl.y_start + 1 - overlaps[1]
        remainder_cuboid_x = self.x_stop - self.x_start + 1 - overlaps[2]

        # return remnants_of_self_cuboid, remnants_of_provided_cuboid
        pass


###########
#  funcs  #
###########


def gen_3d_matrix(z_size: int, y_size: int, x_size: int) -> list:
    matrix = []
    for z in range(101):
        z_dimension = []
        for y in range(101):
            y_dimension = []
            for x in range(101):
                y_dimension.append(0)
            z_dimension.append(y_dimension)
        matrix.append(z_dimension)

    return matrix


###########
#  parts  #
###########


def part1():
    # init a stating 3d matrix with all locations marked as off
    # size is -50 to 50 in all dimensions... matrix[z][y][x]
    matrix = gen_3d_matrix(101, 101, 101)

    for instruction in instructions:
        # translate coordinates to be from a point of origin at 50 (x, y, & z)
        # and strip off points outside of our matrix by setting mins & maxs
        # TODO: this can likely be done on the fly rather than setting vars...
        x_start = max([instruction['x_start'] + 50, 0])
        x_stop  = min([instruction['x_stop'] + 50, 101])
        y_start = max([instruction['y_start'] + 50, 0])
        y_stop  = min([instruction['y_stop'] + 50, 101])
        z_start = max([instruction['z_start'] + 50, 0])
        z_stop  = min([instruction['z_stop'] + 50, 101])

        # set the action
        action = 1 if instruction['action'] == 'on' else 0

        # generate locations for all poistions within 3d ranges
        positions = []
        for z in range(z_start, z_stop + 1):
            for y in range(y_start, y_stop + 1):
                for x in range(x_start, x_stop + 1):
                    positions.append((z, y, x))

        # perform operation on positions and update matrix state
        for pos in positions:
            # print('turning', action, pos)
            matrix[pos[0]][pos[1]][pos[2]] = action

    # add up all our ons
    sum = 0
    for z in matrix:
        for y in z:
            sum += y.count(1)

    return sum


def part2():
    # converst all our instructions to a list of objects
    cubed_instructions = [Cuboid(inst) for inst in instructions]

    # start a list to store our resulting cuboids
    cuboids = []

    # loop through each instruction
    for i in cubed_instructions:
        # start a list of cuboids that we need to appen into the cuboids list
        to_extend = []

        # compare our current cuboid to all cuboids in cuboids list
        for c in cuboids:
            # if our current instruction cuboid and the cuboid from the list
            # overlap grab the overlap (a cuboid itself), the overlap method
            # will determine whether this is an on or off cuboid, take a look
            if i.intersects(c):
                to_extend.append(i.overlap(c))

        # extend our cuboids list with the new overlap cuboids
        cuboids.extend(to_extend)

        # and lastly if we are looking at an on instruction, append to cuboids
        if i.action == 'on':
            cuboids.append(i)

    # count up on cuboids from cuboids list by adding on's and subtracting offs
    count = 0
    for c in cuboids:
        if c.action == 'on':
            count += c.volume
        else:
            count -= c.volume

    return count


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
