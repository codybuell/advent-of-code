#!/usr/bin/env python3
# https://adventofcode.com/2020/day/15

import re
import math
import time
import collections

dataFile = open('day-15.txt', 'r')
initSeq  = dataFile.read().rstrip().split(',')

def part1(count):
    seq = initSeq.copy()
    i = len(seq) + 1
    while True:
        lastNumSpoken = seq[-1]
        timesSpoken   = seq.count(lastNumSpoken)

        # if it's been said before now find gap, else 0
        if timesSpoken > 1:
            # reverse the sequence, slice of first el, find index target
            # then add one to find the times since it was last spoken
            timesSinceLastSpoken = seq[-2::-1].index(lastNumSpoken) + 1
            toAppend = timesSinceLastSpoken
        else:
            toAppend = 0

        seq.append(str(toAppend))

        if i == count:
            print(toAppend)
            return toAppend

        i += 1

def part2mk1(count):
    seq  = initSeq.copy()
    i    = len(seq) + 1
    while True:
        lastNumSpoken = seq[-1]
        timesSpoken   = seq.count(lastNumSpoken)

        # pop off elements from list if possible...
        while True:
            if seq.count(seq[0]) > 2:
                seq.pop(0)
            else:
                break

        # if it's been said before now find gap, else 0
        if timesSpoken > 1:
            # reverse the sequence, slice of first el, find index target
            # then add one to find the times since it was last spoken
            timesSinceLastSpoken = seq[-2::-1].index(lastNumSpoken) + 1
            toAppend = timesSinceLastSpoken
        else:
            toAppend = 0

        seq.append(str(toAppend))

        if i == count:
            print(toAppend)
            return toAppend

        i += 1

def part2mk2(count):
    # convert our list to ints
    # reverse our sequence and create a deque for fast appendleft
    # initialize our count so we know when we're at our target
    # first append is always a 0, so lets start with that
    # initialize a set for fast checking of spoken numbers
    to_int = [int(x) for x in initSeq]
    seq    = collections.deque(to_int[::-1])
    i      = len(seq) + 1
    upnext = 0
    spoken = set(seq)

    # run it until our target count then spit out the number
    while True:
        if i == count:
            print(upnext)
            return upnext

        # if our number to append has been spoken before get the index
        if upnext in spoken:
            # print('index of last instance: ', seq.index(upnext))
            # then add one to find the times since it was last spoken
            nexttoapend = seq.index(upnext) + 1
        else:
            nexttoapend = 0

        # append left to our deque
        # add to spoken set
        # set next to check
        # increment
        seq.appendleft(upnext)
        spoken.add(upnext)
        upnext = nexttoapend
        i += 1

def part2mk3(count,diff_time):
    # convert our list to ints
    # reverse our sequence and create a deque for fast appendleft
    # initialize our count so we know when we're at our target
    # first append is always a 0, so lets start with that
    # initialize a set for fast checking of spoken numbers
    to_int = [int(x) for x in initSeq]
    seq    = collections.deque(to_int[::-1])
    i      = len(seq) + 1
    upnext = 0
    spoken = set(seq)

    # run it until our target count then spit out the number
    while True:
        if i == count:
            print(upnext)
            return upnext

        if i % 100000 == 0:
            print(i,'-', (time.time() - start_time), '(', (time.time() - diff_time), ')')
            diff_time  = time.time()

        # if our number to append has been spoken before get the index
        if upnext in spoken:
            # print('index of last instance: ', seq.index(upnext))
            # then add one to find the times since it was last spoken
            nexttoapend = seq.index(upnext) + 1
            seq.appendleft(upnext)
            spoken.add(upnext)
            upnext = nexttoapend
            i += 1
        else:
            # here we can make two steps in one go
            seq.appendleft(upnext)
            spoken.add(upnext)
            upnext = seq.index(0) + 1
            seq.appendleft(0)
            i += 2

        # # optimize our seq by removing last digit if there are more than 2
        # while True:
        #     if seq.count(seq[-1]) > 2:
        #         seq.pop()
        #     else:
        #         break

def part2mk4(count,diff_time):
    seq   = {int(x):idx for idx,x in enumerate(initSeq)}
    i     = len(seq)
    upnxt = 0

    while True:
        if i + 1 == count:
            print('>>',upnxt)
            return upnxt

        if i % 100000 == 0:
            print(i,'-', (time.time() - start_time), '(', (time.time() - diff_time), ')')
            diff_time  = time.time()

        if upnxt in seq:
            nexttochk = i - seq[upnxt]
        else:
            nexttochk = 0

        seq[upnxt] = i
        upnxt = nexttochk

        i += 1

if __name__ == "__main__":

    # part1(2020)       runs in 0.059381961822509766 seconds
    # part2mk1(2020)    runs in 0.10097789764404297 seconds
    # part2mk2(2020)    runs in 0.0041429996490478516 seconds
    # part2mk3(2020)    runs in 0.03568673133850098 seconds

    # part1(100000)     runs in (not gonna bother)
    # part2mk1(100000)  runs in 243.6219699382782
    # part2mk2(100000)  runs in 5.188076734542847
    # part2mk3(100000)  runs in 84.74193382263184 (with seq dedupe)
    # part2mk3(100000)  runs in 5.211131811141968 (w/o seq dedupe)

    # part2mk4(100000, diff_time) runs in 0.04338788986206055 sec << winner

    part1(2020)
    start_time = time.time()
    diff_time  = time.time()
    part2mk4(30000000, diff_time)
    print("--- %s seconds ---" % (time.time() - start_time))
