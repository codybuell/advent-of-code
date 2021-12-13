#!/usr/bin/env python
# https://adventofcode.com/2021/day/13


import re


###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
y_coords = []
x_coords = []
folds = []
for line in lines:
    p_coord = re.compile(r"(\d*),(\d*)")
    p_fold  = re.compile(r"fold along ([xy])=(\d+)")

    m_coord = re.match(p_coord, line)
    m_fold  = re.match(p_fold, line)

    if m_coord:
        x_coords.append(int(m_coord[1]))
        y_coords.append(int(m_coord[2]))

    if m_fold:
        folds.append([m_fold[1], int(m_fold[2])])

# get extent of paper, draw out all 0's then populate our coords with 1's
paper = []
y_max = max(y_coords) + 1
x_max = max(x_coords) + 1
for y in range(y_max):
    paper.append([])
    for x in range(x_max):
        paper[y].append(0)
for i in range(len(y_coords)):
    paper[y_coords[i]][x_coords[i]] = 1


###########
#  funcs  #
###########


def print_sheet(sheet: list):
    print()
    for line in sheet:
        print(''.join([str(x) for x in line]).replace("1", "#").replace("0", "."))
    print()


def fold(along: str, pos: int, paper: list) -> list:
    # if folding on y
    if along == 'y':
        # measure lines above and below, padd with 0's accordingly
        sheet_one = paper[0:pos]                         # upper paper
        sheet_two = paper[pos + 1:]                      # lower paper
        diff      = len(sheet_one) - len(sheet_two)

        if abs(diff):
            padd = [[0 for i in range(x_max)] for i in range(abs(diff))]
            if diff > 0:
                sheet_two.extend(padd)
            else:
                padd.extend(sheet_one)
                sheet_one = padd

        # reverse lower portion order
        sheet_two.reverse()

    # elif folding on x
    elif along == 'x':
        # measure lines left and right, padd with 0's accordingly
        sheet_one = [x[0:pos] for x in paper]            # left sheet
        sheet_two = [x[pos + 1:] for x in paper]         # right sheet
        diff      = len(sheet_one[0]) - len(sheet_two[0])

        if abs(diff):
            to_extend = [0 for i in range(abs(diff))]
            if diff > 0:
                for idy, y in enumerate(sheet_two):
                    sheet_two[idy].extend(to_extend)
            else:
                for idy, y in enumerate(sheet_one):
                    to_extend.extend(y)
                    sheet_one[idy] = to_extend

        # reverse right side order
        for idy, y in enumerate(sheet_two):
            y.reverse()
            sheet_two[idy] = y

    # perform the fold (just need to overlay sheet_one and sheet_two)
    folded_paper = []
    for y in range(len(sheet_two)):
        folded_paper.append([])
        for x in range(len(sheet_two[0])):
            folded_paper[y].append(1 if sheet_one[y][x] + sheet_two[y][x] else 0)

    return folded_paper


###########
#  parts  #
###########


def part1():
    # just run the first fold
    folded_paper = fold(folds[0][0], folds[0][1], paper)
    visible_dots = 0
    for line in folded_paper:
        for x in line:
            visible_dots += int(x)

    return visible_dots


def part2():
    folded_paper = paper.copy()
    for inst in folds:
        folded_paper = fold(inst[0], inst[1], folded_paper)

    print_sheet(folded_paper)


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:')
    part2()
