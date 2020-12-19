#!/usr/bin/env python3
# https://adventofcode.com/2020/day/18

import re
import sys

dataFile    = open('day-18.txt', 'r')
expressions = dataFile.read().splitlines()
expression = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"

def eval_left_to_right(expression):
    while True:
        to_eval = re.search('(\d+\s*[^\d\s]\s*\d+|\(\d+\s*[^\d\s]\s*\d+\))', expression)
        if to_eval is not None:
            value = eval(to_eval.group())
            expression = expression[0:to_eval.start()] + str(value) + expression[to_eval.end():]
        else:
            return int(expression)

def eval_ltr_sum_then_prod(expression):

    # deal with as many additions as we can or parens containing only one prod, or parens containing only many prods
    # else we are just reduced to an expression containing multiplications, so evaluate that ant return
    while True:
        to_eval = re.search('(\d+\s*\+\s*\d+|\(\d+\s*\*\s*\d+\)|\([\d\s\*]+\))', expression)
        if to_eval is not None:
            value = eval(to_eval.group())
            expression = expression[0:to_eval.start()] + str(value) + expression[to_eval.end():]
        else:
            return(eval(expression))

def part1():
    total = 0
    for exp in expressions:
        total += eval_left_to_right(exp)
    print(total)

def part2():
    total = 0
    for exp in expressions:
        total += eval_ltr_sum_then_prod(exp)
    print(total)

if __name__ == "__main__":
    part1()
    part2()
