#!/usr/bin/env python3
# https://adventofcode.com/2020/day/16

import re

dataFile = open('day-16.txt', 'r')
sections = dataFile.read().split('\n\n')

def parseData():
    # parse rules
    rules = []
    p = re.compile('(^[^:]*):\s*(\d*)-(\d*)\s*or\s*(\d*)-(\d*)$')
    for line in sections[0].split('\n'):
        m = re.match(p, line)
        r1 = range(int(m.group(2)), int(m.group(3)) + 1)
        r2 = range(int(m.group(4)), int(m.group(5)) + 1)
        rule = {
                'name': m.group(1),
                'rules': [r1, r2],
                'values': list(r1) + list(r2)
                }
        rules.append(rule)

    # parse your ticket
    ticket = [int(x) for x in sections[1].split('\n')[1].rstrip().split(',')]

    # parse other tickets
    tickets = []
    for line in sections[2].rstrip().split('\n')[1:]:
        tickets.append([int(x) for x in line.split(',')])

    return rules, ticket, tickets

def part1():
    rules, ticket, tickets = parseData()

    # look through each ticket for bad values
    badValues = []
    goodTickets = []
    for ticket in tickets:
        # for each value see if it follows a rule
        good = True
        for value in ticket:
            found = False
            for ruleset in rules:
                if value in ruleset['values']:
                    found = True
                    break

            if not found:
                badValues.append(value)
                good = False
                break

        if good:
            goodTickets.append(ticket)

    return sum(badValues), goodTickets

def part2(goodTickets):

    # get our data
    rules, myticket, tickets = parseData()

    # moosh our ticket into the good tickets list
    goodTickets.append(myticket)

    # for each indexed ticket value build a list of possible rules, if rule is
    # valid for every ticket[N] value then add to list
    validRulesForValueIndex = []
    for i in range(len(myticket)):
        validRules = []
        for rule in rules:
            fit = True
            for ticket in goodTickets:
                if ticket[i] not in rule['values']:
                    fit = False
                    break
            if fit:
                validRules.append(rule['name'])
        validRulesForValueIndex.append(validRules)

    # if any index in validRulesForValueIndex has a len of one that is a match,
    # set it's location and value in fields{}, then remove it from every other
    # validRulesForValueIndex entry and repeat, loop till we've got it all
    fields = {}
    while len(fields) != len(myticket):
        for idx, i in enumerate(validRulesForValueIndex):
            if len(i) == 1:
                fields[idx] = i[0]
                # remove i[0] from all other i in validRulesForValueIndex
                for idxj, j in enumerate(validRulesForValueIndex):
                    if idxj != idx:
                        if i[0] in j:
                            j.remove(i[0])

    # mush our ticket with the field names
    mymappedticket = {}
    for idx,i in enumerate(myticket):
        mymappedticket[fields[idx]] = i

    # grab values for fields that start with departure
    prod = 1
    for i in mymappedticket:
        if re.match('^departure.*$', i):
            prod *= mymappedticket[i]

    print(prod)

if __name__ == "__main__":
    sumBadValues, goodTickets = part1()
    print('>>', sumBadValues)
    part2(goodTickets)
