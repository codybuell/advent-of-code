#!/usr/bin/env python3
# https://adventofcode.com/2020/day/11

import os
import re
import sys
import time
import curses
import itertools

dataFile = open('day-11.txt', 'r')
lines    = dataFile.read().splitlines()
xRange   = len(lines) - 1
yRange   = len(lines[0]) - 1
cursesOn = True

def seatsAround1(seat, seatsMatrix):
    # seat -> [x,y]
    checkRange = range(-1,2)

    # build a list of all locations around seat, account for edge limits
    aroundCoords = [[min(xRange, max(0,seat[0] + x)), min(yRange, max(0,seat[1] + y))] for x in checkRange for y in checkRange]

    # remove duplicates from list
    aroundCoords.sort()
    aroundCoords = [aroundCoords for aroundCoords,_ in itertools.groupby(aroundCoords)]

    # remove the seat itself
    aroundCoords.remove(seat)

    # get values of those locations
    aroundValues = [seatsMatrix[i[0]][i[1]] for i in aroundCoords]

    return aroundCoords, aroundValues

def seatsAround2(seat, seatsMatrix):
    # seat -> [x,y]

    # get surrounding coords and values
    aroundCoords, aroundValues = seatsAround1(seat, seatsMatrix)

    # detimine target seats and their values by radiating out on each vector till match
    targetCoords = []
    targetValues = []
    for idx, i in enumerate(aroundCoords):
        # check the immediate surrounding for a chair so we don't have to walk a vector
        if re.match('(L|#)', aroundValues[idx]):
            targetCoords.append(i)
            targetValues.append(aroundValues[idx])
            continue

        # otherwise determine vector to check
        plusX = i[0] - seat[0]
        plusY = i[1] - seat[1]

        # walk the vector till we find a seat
        checkX = i[0] + plusX
        checkY = i[1] + plusY

        while True:
            # ensure our point is within the matrix, else break
            if checkX in range(xRange + 1) and checkY in range(yRange + 1):
                # if we find a seat, append it's info and break
                checkValue = seatsMatrix[checkX][checkY]
                if re.match('(L|#)', checkValue):
                    targetCoords.append([checkX, checkY])
                    targetValues.append(checkValue)
                    break

                # else increment by our vector
                checkX += plusX
                checkY += plusY
            else:
                break

    return targetCoords, targetValues

def life(seatsMatrix, aroundRule, tolerance):
    newSeatsMatrix = seatsMatrix.copy()
    for idx, row in enumerate(seatsMatrix):
        for idy, col in enumerate(row):
            seatValue        = seatsMatrix[idx][idy]

            # ignore floor space
            if seatValue == '.':
                continue

            aCoords, aValues = aroundRule([idx,idy], seatsMatrix)
            occupiedAround   = aValues.count('#')

            if seatValue == '#' and occupiedAround >= tolerance:
                # if seat is occupied, unoccupy if N or more surrounding seats are occupied
                seatValue = 'L'
            elif occupiedAround == 0:
                # else if no seat around current seat is occupied, occupy it
                seatValue = '#'

            newSeatsMatrix[idx] = newSeatsMatrix[idx][:idy] + seatValue + newSeatsMatrix[idx][idy + 1:]

    # print out the matrix and stats
    occupied = 0
    for idi, i in enumerate(newSeatsMatrix):
        occupied += i.count('#')
        if cursesOn:
            stdscr.addstr(idi, 0, i)
            if idi == xRange:
                stdscr.addstr(idi + 1, 0, '')
                stdscr.addstr(idi + 2, 0, str(occupied) + ' occupied')
            stdscr.refresh()

    if cursesOn:
        curses.echo()
        curses.nocbreak()
        #time.sleep(1/100)

    # if no diff between seatsMatrix and newSeatsMatrix we are done, return occupied seats
    if newSeatsMatrix == seatsMatrix:
        if not cursesOn:
            print("seats occupied: " + str(occupied))
        return

    # else rerun with new matrix
    life(newSeatsMatrix, aroundRule, tolerance)

if __name__ == "__main__":
    if cursesOn:
        rows, columns = os.popen('stty size', 'r').read().split()
        if int(columns) < yRange or int(rows) < xRange + 3:
            print('screen needs to be larger for seating chart to display')
            cursesOn = False
        else:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

    # part 1
    life(lines, seatsAround1, 4)

    if cursesOn:
        time.sleep(5)

    # part 2
    life(lines, seatsAround2, 5)

    if cursesOn:
        # return terminal to normal
        time.sleep(5)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
