#!/usr/bin/env python
# https://adventofcode.com/2021/day/24

import re
import sys
# import threading

###########
#  setup  #
###########


# ingest data
dataFile = open('sample.txt', 'r')
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


def brute_force(start: int, stop: int):
    # work backwards, define our highes possible model number
    model_number = start

    # create a copy of ram so we don't step on other threads
    ram = {
        'p': 0,        # pointer to index of digit in model number
        'w': None,     # address w
        'x': None,     # address x
        'y': None,     # address y
        'z': None,     # address z
    }

    while True:
        # reset our ram to test this model number
        reset_ram(ram)

        # convert our model number into a list of ints
        model_num_list = [int(x) for x in list(str(model_number))]
        ram['model_number'] = model_num_list

        # handle any 0's in our starting number
        if 0 in model_num_list:
            model_number = reduce_model_number(model_number)
            continue

        # run each digit through our monad application
        for i in instructions:
            eval(i)

        # after running each digit check for validity
        if ram['z'] == 0:
            # prGreen(str(model_number) + ' : ' + str(ram['w']) + str(ram['x']) + str(ram['y']) + str(ram['z']))
            print('for range', start, 'to', stop, ':', model_number)
            return model_number
        else:
            # prRed(str(model_number) + ' : ' + str(ram['w']) + str(ram['x']) + str(ram['y']) + str(ram['z']))
            # reduce our model number
            model_number = reduce_model_number(model_number)
            if model_number is None:
                print('model number is less than 14 digits')
                return
            if model_number < stop:
                print('completed range', start, 'to', stop)
                return


def rev_inp(a, ram):
    pass


def rev_add(a, b, ram):
    """ Add the values of a to the value of b. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = va - vb


def rev_mul(a, b, ram):
    """ Multiply the values of a by b. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = va / vb


def rev_div(a, b, ram):
    """ Divide the values of a by b, round towards 0. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    # if vb == 0:
    #     print("error: divide by 0")
    #     sys.exit()
    ram[a] = va * vb


def rev_mod(a, b, ram):
    pass


def rev_eql(a, b, ram):
    """ Compare a to b, 1 if equal, 0 if not. Store in a. """
    va = 0 if ram[a] is None else ram[a]
    vb = process_arg(b, ram)
    ram[a] = vb if va == 1 else 4    # else could be any value??


###########
#  parts  #
###########


def part1():

    ##########################
    #  threaded brute force  #
    ##########################
    """ Check all possible values high to low, broken into threads. """

    # # define highest and lowest possible values
    # highest = 99999999999999
    # lowest  = 11111111111111

    # # thread count
    # count = 300

    # # define our threads
    # threads = []
    # increments = (highest - lowest) / count
    # for i in range(count):
    #     a = highest - (i * increments)
    #     b = highest - ((i + 1) * increments)
    #     t = threading.Thread(target=brute_force, args=(int(a), int(b)))
    #     t.start()
    #     threads.append(t)

    # # wait until all our threads are complete
    # for t in threads:
    #     t.join()

    ############################
    #  unthreaded brute force  #
    ############################
    """ Check all possible values high to low sequentially. """

    # # define highest and lowest possible values
    # highest = 99999999999999
    # lowest  = 11111111111111

    # # run them all...
    # brute_force(highest, lowest)

    ################################
    #  work instruction backwards  #
    ################################

    # load up our ram with a desired state
    ram = {
        'p': 0,        # pointer to index of digit in model number
        'w': None,     # address w
        'x': None,     # address x
        'y': None,     # address y
        'z': 0,        # address z
    }

    instructions.reverse()
    for i in instructions:
        eval('rev_' + i)


def part2():
    pass


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
