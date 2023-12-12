#!/usr/bin/env python3
# https://adventofcode.com/2023/day/2

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

games = {}
for line in lines:
    pGame = re.compile(r"Game\s(\d+):(.*)")
    pCube = re.compile(r"\s(\d+)\s(\S+)")
    m = re.match(pGame, line)
    gameNumber = m.group(1)
    sets = m.group(2).split(';')
    gameSets = []
    for s in sets:
        cubes = s.split(',')
        thisSet = {}
        for c in cubes:
            mCube = re.match(pCube, c)
            thisSet[mCube.group(2)] = int(mCube.group(1))
        gameSets.append(thisSet)
    games[gameNumber] = gameSets


def part1():
    cubes = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    possible = []

    for gameNumber, sets in games.items():
        # get the max  rawn for each color
        m = {}
        for s in sets:
            comp = {key: max(value, m.get(key) or 0) for key, value in s.items()}
            for color, count in comp.items():
                m[color] = count

        # determine if any draws were over the cube set
        possibleGame = True
        for color, count in cubes.items():
            if m[color] > count:
                possibleGame = False
                break

        if possibleGame:
            possible.append(int(gameNumber))

    print(sum(possible))


def part2():
    powers = []
    for gameNumber, sets in games.items():
        # get the max  rawn for each color
        m = {}
        for s in sets:
            comp = {key: max(value, m.get(key) or 0) for key, value in s.items()}
            for color, count in comp.items():
                m[color] = count

        prod = 1
        for _, count in m.items():
            prod = prod * count

        powers.append(prod)

    print(sum(powers))


part1()
part2()
