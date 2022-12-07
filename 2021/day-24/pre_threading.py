#!/usr/bin/env python
# https://adventofcode.com/2021/day/24

import re
import sys

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
instructions = []
p = re.compile(r"^([^\s]+)\s(.*$)")
for line in lines:
    m = re.match(p, line)
    actn = m.group(1)
    args = m.group(2).split()
    args[0] = "'" + args[0] + "'"
    if len(args) == 2:
        args[1] = "'" + args[1] + "'" if args[1].isalpha() else args[1]
    instructions.append("%s(%s, ram)" % (actn, ','.join(args)))


###########
#  funcs  #
###########


def prRed(skk, lineend='\n'):
    print("\033[91m {}\033[00m" .format(skk), end=lineend)


def prGreen(skk, lineend='\n'):
    print("\033[92m {}\033[00m" .format(skk), end=lineend)


def reset_ram(ram):
    """ Fully clear the ram. """
    ram['p'] = 0
    ram['w'] = None
    ram['x'] = None
    ram['y'] = None
    ram['z'] = None


def process_arg(a, ram):
    """ Returns value from address in ram if a is an address, else the value that it is. """
    if type(a) == int:
        return a
    else:
        return 0 if ram[a] is None else ram[a]


def inp(a, ram):
    """ Read the i value and assign it to a. """
    ram[a] = ram['model_number'][ram['p']]
    ram['p'] += 1


def add(a, b, ram):
    """ Add the values of a to the value of b. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = va + vb


def mul(a, b, ram):
    """ Multiply the values of a by b. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = va * vb


def div(a, b, ram):
    """ Divide the values of a by b, round towards 0. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    if vb == 0:
        print("error: divide by 0")
        sys.exit()
    ram[a] = va // vb


def mod(a, b, ram):
    """ Modulo a by b. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    if va < 0 or vb <= 0:
        print("error: modulo a < 0 or b <= 0")
        sys.exit()
    ram[a] = va % vb


def eql(a, b, ram):
    """ Compare a to b, 1 if equal, 0 if not. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = 1 if va == vb else 0


def reduce_model_number(number: int) -> int:
    # reduce it by 1
    number -= 1

    # keep reducing until we have no 0's
    while True:
        num_list = [int(x) for x in list(str(number))]

        # stop when we have no more 0's in our number
        if 0 not in num_list:
            return number

        # or if our number is less than 14 digits
        if len(num_list) < 14:
            return None

        num_list.reverse()

        # find the first 0 digit from right to left
        # if last digit is 0 then -1 again
        # if second to last digit is 0 -10
        # if third to last digit is 0 - 100 eg 9099
        # etc...
        for idx, digit in enumerate(num_list):
            if digit == 0:
                number -= 10 ** idx
                break

    # for n in [9, 8, 7, 6, 5, 4, 3, 2]:
    #     for idx, num in enumerate(number):
    #         if num == n:
    #             number[idx] -= 1
    #             return int(''.join([str(x) for x in number]))


###########
#  parts  #
###########


def part1():

    # setup state, store it in ram
    ram = {
        'p': 0,        # pointer to index of digit in model number
        'w': None,     # address w
        'x': None,     # address x
        'y': None,     # address y
        'z': None,     # address z
    }

    # work backwards, define our highes possible model number
    model_number = 99999999999999

    while True:
        # reset our ram to test this model number
        reset_ram(ram)

        # convert our model number into a list of ints and store in ram
        model_num_list = [int(x) for x in list(str(model_number))]
        ram['model_number'] = model_num_list

        # run each digit through our monad application
        for i in instructions:
            eval(i)

        # after running each digit check for validity
        if ram['z'] == 0:
            prGreen(str(model_number) + ' : ' + str(ram['w']) + str(ram['x']) + str(ram['y']) + str(ram['z']))
            return model_number
        else:
            prRed(str(model_number) + ' : ' + str(ram['w']) + str(ram['x']) + str(ram['y']) + str(ram['z']))
            # reduce our model number
            model_number = reduce_model_number(model_number)
            if model_number is None:
                print('modell number is less than 14 digits')
                sys.exit()


def part2():
    pass


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
