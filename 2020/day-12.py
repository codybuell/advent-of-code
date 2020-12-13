#!/usr/bin/env python3
# https://adventofcode.com/2020/day/12
# can you override the boat class rather than rewriting?

import re

dataFile   = open('day-12.txt', 'r')
lines      = dataFile.read().splitlines()

class Boat():
    # directions: 0 north, 1 east, 2 south, 3 west
    direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    # initial conditions
    position = [0, 0]
    heading  = 1

    def move(self, code):
        code  = re.match('(\D{1})(\d*)', code)
        a = code.group(1)
        v = int(code.group(2))
        if a == 'N':
            self.travel([0, v])
        elif a == 'S':
            self.travel([0, -v])
        elif a == 'E':
            self.travel([v, 0])
        elif a == 'W':
            self.travel([-v, 0])
        elif a == 'L':
            self.rotate(-v)
        elif a == 'R':
            self.rotate(v)
        elif a == 'F':
            x = self.direction[self.heading][0] * v
            y = self.direction[self.heading][1] * v
            self.travel([x, y])

    def travel(self, motion):
        self.position = [a + b for (a, b) in zip(self.position, motion)]

    def rotate(self, degrees):
        increment = int((degrees / 90) % 4)
        self.heading = int((self.heading + increment) % 4)

    def manhattan(self):
        print('distance: ' + str(abs(self.position[0]) + abs(self.position[1])))


class Boat2():
    # initial conditions
    waypoint = []
    position = [0, 0]

    def __init__(self, coords):
        self.waypoint = coords

    def update(self, code):
        code  = re.match('(\D{1})(\d*)', code)
        a = code.group(1)
        v = int(code.group(2))
        if a == 'N':
            self.shift([0, v])
        elif a == 'S':
            self.shift([0, -v])
        elif a == 'E':
            self.shift([v, 0])
        elif a == 'W':
            self.shift([-v, 0])
        elif a == 'L':
            self.rotate(-v)
        elif a == 'R':
            self.rotate(v)
        elif a == 'F':
            x = self.waypoint[0] * v
            y = self.waypoint[1] * v
            self.travel([x, y])

    def shift(self, motion):
        self.waypoint = [a + b for (a, b) in zip(self.waypoint, motion)]

    def travel(self, motion):
        self.position = [a + b for (a, b) in zip(self.position, motion)]

    def rotate(self, degrees):
        rotationsRight = int((degrees / 90) % 4)
        if rotationsRight == 1:
            self.waypoint = [self.waypoint[1], self.waypoint[0] * -1]
        elif rotationsRight == 2:
            self.waypoint = [self.waypoint[0] * -1, self.waypoint[1] * -1]
        elif rotationsRight == 3:
            self.waypoint = [self.waypoint[1] * -1, self.waypoint[0]]

    def manhattan(self):
        print('distance: ' + str(abs(self.position[0]) + abs(self.position[1])))

def part1():
    boat = Boat()
    for i in lines:
        boat.move(i)
    print("boat is at: " + str(boat.position))
    print("boat is facing: " + str(boat.heading))
    boat.manhattan()

def part2():
    boat = Boat2([10, 1])
    for i in lines:
        boat.update(i)
    print("boat is at: " + str(boat.position))
    boat.manhattan()

if __name__ == "__main__":
    part1()
    print('==================')
    part2()
