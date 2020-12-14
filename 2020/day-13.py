#!/usr/bin/env python3
# https://adventofcode.com/2020/day/13

import re
import math

dataFile = open('day-13.txt', 'r')
lines    = dataFile.read().splitlines()

def part1():
    target = int(lines[0])
    busses = [int(x) for x in lines[1].split(',') if x != 'x']

    # longest possible wait time is slowest bus if you just missed it
    longest = max(busses)

    # iterate over each bus till we are in range of target and longest
    nextTime = []
    for bus in busses:
        i = 0
        t = 0
        while t not in range(target, target + longest):
            t  = i * bus
            i += 1
        nextTime.append(t)

    # run some numbers
    minTime   = min(nextTime)
    minBusIdx = nextTime.index(min(nextTime))
    minBus    = busses[minBusIdx]
    waitTime  = minTime - target
    print(minBus * waitTime)

def part2():
    # brute force approach, takes days? to run
    busses          = lines[1].split(',')
    keyBusDeparture = int(busses[0])
    while True:
        badSequence = False

        # check all other bus times
        for idx, bus in enumerate(busses[1:]):
            if bus == 'x':
                continue
            else:
                bus = int(bus)

            # targetTime = (keyBusDeparture + idx + 1)
            # if targetTime % bus != 0:
            #     badSequence = True
            #     break

            nextPossibleDeparture = math.ceil(keyBusDeparture / bus) * bus

            # print('bus zero departure: ' + str(keyBusDeparture))
            # print('bus index: ' + str(idx + 1))
            # print('its next departure time: ' + str(nextPossibleDeparture))

            # if next bus departure does not follow seq
            if nextPossibleDeparture != (keyBusDeparture + idx + 1):
                badSequence = True
                break

        if badSequence:
            # print('caught bad seq')
            keyBusDeparture += int(busses[0])
            continue
        else:
            print(keyBusDeparture)
            break

def part2mk2():
    # chinese remainder theorem

    # make a list of our busses from the input
    busses = lines[1].split(',')

    # build list of bus id tuples (adjusted id for index, orig id)
    bussIds = []
    for idx, bus in enumerate(busses):
        if bus == 'x':
            continue
        bussIds.append((int(bus) - idx, int(bus)))

    # multiply all original bus id's together
    prod = 1
    for adj, og in bussIds:
        prod *= og

    # calculate our initial bus time
    initialTime = 0
    for adj, og in bussIds:
        b = prod // og
        initialTime += adj * b * ((b**(og-2)) % og) 
        initialTime %= prod

    print(initialTime)

if __name__ == "__main__":
    part1()
    #part2()
    part2mk2()
