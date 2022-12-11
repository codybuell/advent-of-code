#!/usr/bin/env python3
# https://adventofcode.com/2022/day/11

import os
import math
from copy import deepcopy

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# build a list of monkeys
monkeys = [[]]
for line in lines:
    if line == '':
        monkeys.append([])
        continue
    monkeys[len(monkeys) - 1].append(line)

# init some vars to track state
monkey_state = {}

# run through each monkey to derive state
for monkey in monkeys:
    monkey_number  = monkey[0].split(' ')[-1].replace(':', '')
    starting_items = [x.strip() for x in monkey[1].split(':')[-1].split(',')]
    operation      = monkey[2].split('=')[-1].strip()
    test           = monkey[3].split(':')[-1].strip()
    if_true        = monkey[4].split(' ')[-1]
    if_false       = monkey[5].split(' ')[-1]

    monkey_state[monkey_number] = {
        'items': starting_items,
        'operation': operation,
        'test': test,
        'if_true': if_true,
        'if_false': if_false,
        'inspections': 0,
    }

################################################################################
##                                                                            ##
##  Part 1                                                                    ##
##                                                                            ##
################################################################################


def part_1(state: dict, rounds):
    # iterate through 'rounds'
    for round in range(rounds):
        for monkey, deets in state.items():
            if len(deets['items']):
                for item in deets['items']:
                    op = deets['operation'].replace('old', item)
                    # monkey inspects
                    worry = eval(op)
                    deets['inspections'] += 1
                    # we chill out
                    worry = int(worry / 3)
                    # monkey inspects worry level
                    if worry % int(deets['test'].split(' ')[-1]) == 0:
                        state[deets['if_true']]['items'].append(str(worry))
                    else:
                        state[deets['if_false']]['items'].append(str(worry))

                deets['items'] = []

        # print('Round', round + 1)
        # for monkey, deets in state.items():
        #     print('Monkey', monkey + ':', ','.join(deets['items']))
        # print()

    # calculate 'monkey business'
    inspections = []
    for monkey, deets in state.items():
        inspections.append(deets['inspections'])
    inspections.sort(reverse=True)

    return inspections[0] * inspections[1]


################################################################################
##                                                                            ##
##  Part 2                                                                    ##
##                                                                            ##
################################################################################


def part_2(state: dict, rounds):
    # find lcm of monkey tests
    divisors = []
    for _, deets in state.items():
        divisors.append(int(deets['test'].split(' ')[-1]))
    lcm = math.lcm(*divisors)

    # iterate through 'rounds'
    for round in range(rounds):
        for monkey, deets in state.items():
            if len(deets['items']):
                mod = int(deets['test'].split(' ')[-1])
                for item in deets['items']:
                    op  = deets['operation'].replace('old', item)
                    # monkey inspects
                    worry = eval(op)
                    deets['inspections'] += 1
                    # chill out by reducing worry by mod of lcm of all monkey tests
                    worry = worry % lcm
                    # monkey inspects worry level
                    if worry % mod == 0:
                        state[deets['if_true']]['items'].append(str(worry))
                    else:
                        state[deets['if_false']]['items'].append(str(worry))

                deets['items'] = []

        # print('Round', round + 1)
        # for monkey, deets in state.items():
        #     print('Monkey', monkey, 'inspected', (deets['inspections']), 'items')
        # print()

    # calculate 'monkey business'
    inspections = []
    for monkey, deets in state.items():
        inspections.append(deets['inspections'])
    inspections.sort(reverse=True)

    return inspections[0] * inspections[1]


print('part 1:', part_1(deepcopy(monkey_state), 20))
print('part 2:', part_2(deepcopy(monkey_state), 10000))
