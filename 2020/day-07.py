#!/usr/bin/env python3
# https://adventofcode.com/2020/day/7

import re

dataFile = open('day-07.txt', 'r')
lines    = dataFile.read().splitlines()

def genRuleSet():
    ruleSet = {}

    p1 = re.compile('^(.*) bags contain (.*)$')
    p2 = re.compile('^\s*(\d*) (.*) bag[s]?\s*.?$')

    for line in lines:
        bag      = re.match(p1, line).group(1)
        rules    = re.match(p1, line).group(2).split(',')
        bagRules = {}
        for rule in rules:
            if rule != 'no other bags.':
                count   = re.match(p2, rule).group(1)
                innrbag = re.match(p2, rule).group(2)
                bagRules[innrbag] = count
        ruleSet[bag] = bagRules

    return ruleSet

def canContain(bagColor, ruleSet, validOuterBags=set()):
    for bag in ruleSet:
        for innerBag in ruleSet[bag]:
            bagCount = ruleSet[bag][innerBag]
            if innerBag == bagColor:
                # append a bag that cn hold our bag color
                validOuterBags.add(bag)
                # then recursively find bags that can that one
                canContain(bag,ruleSet,validOuterBags)

    return validOuterBags

def mustContain(bagColor, ruleSet):
    bagCount = 0

    for color in ruleSet[bagColor]:
        bagCount += int(ruleSet[bagColor][color])
        bagCount += mustContain(color, ruleSet) * int(ruleSet[bagColor][color])

    return bagCount

def part1():
    ruleSet = genRuleSet()
    bags    = canContain('shiny gold', ruleSet)
    print(len(bags))

def part2():
    ruleSet = genRuleSet()
    count = mustContain('shiny gold', ruleSet)
    print(count)

if __name__ == "__main__":
    part1()
    part2()
