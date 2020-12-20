#!/usr/bin/env python3
# https://adventofcode.com/2020/day/19

import re
import sys
import regex

# use the regex package for (?R)? recursive regex

dataFile = open('day-19.txt', 'r')
data     = dataFile.read().split('\n\n')

# parse rules input into a dictionary
rules = {}
p = '(^\d*): (.*$)'
for rule in data[0].split('\n'):
    m = re.match(p, rule)
    rules[int(m.group(1))] = m.group(2).replace('"', '')

# then sort them into a list indexed by rule number
#rules = [rules[n] for n in range(len(rules))]

# and then prepare our list of images
images = data[1].splitlines()

def generate_regex_pattern(rule):
    if re.match('a|b', rule):
        return rule

    pattern = '('

    for i in rule.split(' '):
        if i == '|':
            pattern += i
            continue

        idx = int(i)
        pattern += generate_regex_pattern(rules[idx])

    pattern += ')'

    return(pattern)

def generate_regex_pattern_take_two(rule, rule_index):
    if re.match('a|b', rule):
        return rule

    pattern = '('

    # if the rule contains itself we have a loop...
    components = rule.split(' ')
    if str(rule_index) in components:
        index_of_loop = components.index(str(rule_index))
        index_of_pipe = components.index('|')
        if index_of_loop > index_of_pipe:
            # our loop is on the right hand side, regex for this rule should be
            # lhs | rhs_before_loop+ lhs rhs_after_loop+
            lhs = ''
            for i in components[:index_of_pipe]:
                idx = int(i)
                lhs += generate_regex_pattern_take_two(rules[idx], idx)

            rhs = ''
            for i in components[index_of_pipe + 1:]:
                idx = int(i)
                if idx == rule_index:
                    rhs += lhs
                else:
                    rhs += generate_regex_pattern_take_two(rules[idx], idx) + '+'

            pattern += lhs + '|' + rhs
        else:
            # our loop is on the left hand side, regex for this rule should be
            # lhs_before_loop+ rhs lhs_after_looop+ | rhs
            rhs = ''
            for i in components[index_of_pipe + 1:]:
                idx = int(i)
                rhs += generate_regex_pattern_take_two(rules[idx], idx)

            lhs = ''
            for i in components[:index_of_pipe]:
                idx = int(i)
                if idx == rule_index:
                    lhs += rhs
                else:
                    lhs += generate_regex_pattern_take_two(rules[idx], idx) + '+'

            pattern += lhs + '|' + rhs
    else:
        # otherwise handle it as we normally would
        for i in components:
            if i == '|':
                pattern += i
                continue

            idx = int(i)
            pattern += generate_regex_pattern_take_two(rules[idx], idx)

    pattern += ')'

    return(pattern)

def part1():
    # compile our pattern and wrap it in ^$
    pattern = '^' + generate_regex_pattern(rules[0]) + '$'

    count = 0
    for image in images:
        m = re.match(pattern, image)
        if m:
            print(m.group())
            count += 1

    print('===========')
    print(count)

def part2():
    # # take 1 (works for sample, not for puzzle, likey rule 11 needing to by summetrical in recursion
    # # make the corrections to rules from instructions
    # rules[8]  = "42 | 42 8"
    # rules[11] = "42 31 | 42 11 31"
    # # compile our pattern and wrap it in ^$
    # pattern = '^' + generate_regex_pattern_take_two(rules[0], 0) + '$'

    # # take 2 (neither sample or input work here... wtf)
    # # hand jam a regex for rule 0 comprised of two corections
    # p42 = generate_regex_pattern(rules[42])
    # p31 = generate_regex_pattern(rules[31])
    # pattern = '^' + p42 + '+' + p42 + '(?R)?' + p31 + '$'

    # take 3 (the I give up solution)
    # hand jam some iteratinos of rule corrections
    rules[8]  = "42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42 | 42 42 42 42 42 42"
    rules[11] = "42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 | 42 42 42 42 42 31 31 31 31 31 | 42 42 42 42 42 42 31 31 31 31 31 31"
    # compile our pattern and wrap it in ^$
    pattern = '^' + generate_regex_pattern(rules[0]) + '$'

    count = 0
    for image in images:
        m = regex.match(pattern, image)
        if m:
            print(m.group())
            count += 1

    print('===========')
    print(count)

if __name__ == "__main__":
    part1()
    print()
    part2()
