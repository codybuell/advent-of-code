#!/usr/bin/env python
# https://adventofcode.com/2021/day/15

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform data into a 2d matrix
matrix = [list(line) for line in lines]


###########
#  funcs  #
###########


def print_matrix(matrix: list = matrix):
    for line in matrix:
        print(line)


def sort_queue(queue: dict):
    return {k: v for k, v in sorted(queue.items(), key=lambda item: item[1], reverse=True)}


def spaces_orthogonal(coord: list, matrix: list = matrix, add_orig: bool = False) -> list:
    """ Provides all orthogonal spaces around a provided coordinate,
    constrained by the edges of the 2 dmensional matrix. """

    # set some ranges for edge detection
    y_range = len(matrix) - 1
    x_range = len(matrix[0]) - 1

    # define how far out from coord we want to check
    check_range = range(-1, 2)

    # grab rough list of orthogonal coordinates
    orthog_coords = []
    for y_offset in check_range:
        orthog_coords.append([min(y_range, max(0, coord[0] + y_offset)), coord[1]])
    for x_offset in check_range:
        orthog_coords.append([coord[0], min(x_range, max(0, coord[1] + x_offset))])

    # sort and deduplicate them
    orthog_coords.sort()
    orthog_coords = [list(x) for x in set(tuple(x) for x in orthog_coords)]

    # in case we dont want to return the provided coordinate in the list
    if not add_orig:
        orthog_coords.remove(coord)

    return orthog_coords


def spaces_down_and_right(coord: list, matrix: list = matrix, add_orig: bool = False) -> list:
    """ Provides only orthogonal below or to the right of a provided
    coordinate, constrained by the edges of the 2 dmensional matrix. """

    # set some ranges for edge detection
    y_range = len(matrix) - 1
    x_range = len(matrix[0]) - 1

    # define how far out from coord we want to check
    check_range = range(0, 2)

    # grab rough list of orthogonal coordinates
    orthog_coords = []
    for y_offset in check_range:
        orthog_coords.append([min(y_range, max(0, coord[0] + y_offset)), coord[1]])
    for x_offset in check_range:
        orthog_coords.append([coord[0], min(x_range, max(0, coord[1] + x_offset))])

    # sort and deduplicate them
    orthog_coords.sort()
    orthog_coords = [list(x) for x in set(tuple(x) for x in orthog_coords)]

    # in case we dont want to return the provided coordinate in the list
    if not add_orig:
        orthog_coords.remove(coord)

    return orthog_coords


###########
#  parts  #
###########


def part1():
    # size up the matrix
    y_size = len(matrix)
    x_size = len(matrix[0])

    # determine end location
    end_location = str(y_size - 1) + "," + str(x_size - 1)

    # build dict of all positions with their costs to neighbors ordered low to high
    # {
    #     '0,0': {'0,1': 1, '1,0': 1},   # sort sub dict?
    #     '0,1': {'0,0': 1, '0,2': 6},   # ...
    map = {}
    for y in range(y_size):
        for x in range(x_size):
            # set some vars for ease of use
            curpos = str(y) + ',' + str(x)
            map[curpos] = {}

            # get positions orthogonal to current and their values
            around = spaces_orthogonal([y, x])
            values = [matrix[p[0]][p[1]] for p in around]

            # append to our map
            for idx, space in enumerate(around):
                coord_str = ','.join([str(x) for x in space])
                map[curpos][coord_str] = int(values[idx])

            # sort the entry by it's dict values
            map[curpos] = {k: v for k, v in sorted(map[curpos].items(), key=lambda item: item[1])}

    # build a priority queue, some rough approximation of Dijkstra's algorithm
    # init everything with a high cost except 0,0 our starting location
    # cost tracked in queue is cheapest cost to get to key from '0,0'
    queue = {k: 999999999 for k in map}
    queue['0,0'] = 0

    # just in case ensure we sort our queue by value (in reverse so we can popitem())
    queue = sort_queue(queue)

    # build a via dict to track how we got to each location
    via = {k: '' for k in map}

    # assign queue values to neighbors of our starting position and track how we got there
    for neighbor, cost in map['0,0'].items():
        queue[neighbor] = cost
        via[neighbor] = '0,0'
    queue = sort_queue(queue)

    # remove start since we already know how to get there
    finished = {}
    to_append = queue.popitem()
    finished[to_append[0]] = to_append[1]

    # start of loop, look at the next item in queue update costs
    while len(queue):
        next_up = queue.popitem()
        finished[next_up[0]] = next_up[1]

        # look at all the neighbors for our current location (next_up)
        for neighbor, cost in map[next_up[0]].items():
            # we only care about locations still in the queue?
            if neighbor in queue:
                # 999999999 is our cheap representation of infinity, we need to add
                # up costs to get there so set to 0 if it's 'infinity'...
                cur_cost_to_neighbor = queue[neighbor]
                via_cur_loc_to_neighbor = next_up[1] + cost
                # if there is a current cost for the neighbor then we have already
                # found a path to get to it, and we need to compare it with this
                # new path we are currently checking to see which is cheaper
                if cur_cost_to_neighbor > via_cur_loc_to_neighbor:
                    # our new way of getting to the neighbor is cheaper than our
                    # already known path or we've not seen this neighbor before,
                    # update neighbor cost
                    queue[neighbor] = via_cur_loc_to_neighbor
                    via[neighbor] = next_up[0]

        # resort the queue based on new data
        queue = sort_queue(queue)

    return finished[end_location]


def part2():
    # make a copy of the original matrix
    new_matrix = [x[:] for x in matrix]

    # extend it out on x axis
    for y, yval in enumerate(matrix):
        to_extend = []
        for i in range(1, 5):
            for x, xval in enumerate(yval):
                myval = int(xval) + i
                if myval > 9:
                    myval = (myval % 10) + 1
                to_extend.append(str(myval))

        new_matrix[y].extend(to_extend)

    # extend it out on y axis
    to_extend = []
    for i in range(1, 5):
        for y, yval in enumerate(new_matrix):
            to_extend.append([])
            for x, xval in enumerate(yval):
                myval = int(xval) + i
                if myval > 9:
                    myval = (myval % 10) + 1
                to_extend[-1].append(str(myval))

    new_matrix.extend(to_extend)

    ######################## VV TO OPTIMIZE VV #############################
    # This needs work, will run in 2 hours and return correct answer, but...
    # TODO: implement a faster queue
    # TODO: review approach in full
    # TODO: see if you can do something similar to sluff buffer? may not be
    #       needed with a decent queue
    # TODO: remove unnecessary data objects? you are tracking a lot of dicts / lists

    # size up the new matrix
    y_size = len(new_matrix)
    x_size = len(new_matrix[0])

    # determine end location
    end_location = str(y_size - 1) + "," + str(x_size - 1)

    # build dict of all positions with their costs to neighbors ordered low to high
    # {
    #     '0,0': {'0,1': 1, '1,0': 1},   # sort sub dict?
    #     '0,1': {'0,0': 1, '0,2': 6},   # ...
    map = {}
    for y in range(y_size):
        for x in range(x_size):
            # set some vars for ease of use
            curpos = str(y) + ',' + str(x)
            map[curpos] = {}

            # get positions orthogonal to current and their values
            around = spaces_orthogonal([y, x], new_matrix)
            values = [new_matrix[p[0]][p[1]] for p in around]

            # append to our map
            for idx, space in enumerate(around):
                coord_str = ','.join([str(x) for x in space])
                map[curpos][coord_str] = int(values[idx])

            # sort the entry by it's dict values
            map[curpos] = {k: v for k, v in sorted(map[curpos].items(), key=lambda item: item[1])}

    # build a priority queue, some rough approximation of Dijkstra's algorithm
    # init everything with a high cost except 0,0 our starting location
    # cost tracked in queue is cheapest cost to get to key from '0,0'
    queue = {k: 999999999 for k in map}
    queue['0,0'] = 0

    # just in case ensure we sort our queue by value (in reverse so we can popitem())
    queue = sort_queue(queue)

    # build a via dict to track how we got to each location
    # via = {k: '' for k in map}

    # assign queue values to neighbors of our starting position and track how we got there
    for neighbor, cost in map['0,0'].items():
        queue[neighbor] = cost
        # via[neighbor] = '0,0'
    queue = sort_queue(queue)

    # remove start since we already know how to get there
    finished = {}
    to_append = queue.popitem()
    finished[to_append[0]] = to_append[1]

    removed = set()
    removed.add('0,0')

    # start of loop, look at the next item in queue update costs
    while len(queue):
        # print(len(queue))

        next_up = queue.popitem()
        finished[next_up[0]] = next_up[1]

        # # remove coords above and left of current loc from queue...
        # # this currently renders answers too high, as you increase the
        # # sluffbuffer (how many spaces above and left of current position you
        # # keep) the number reduces, the lower the sluffbuffer the faster it
        # # runs by a significant amount, but even with 35 the final answer is
        # # still too high and runs in 52 minutes, 25 -> 42 min, 50 was still
        # # off from final answer by 30... YEAH THIS IS NOT GOING TO WORK
        # sluffbuffer = 35
        # coord = [int(x) - sluffbuffer for x in next_up[0].split(',')]
        # to_rem_from_queue = []
        # for y in range(coord[0]):
        #     for x in range(x_size):
        #         to_rem_from_queue.append(str(y) + ',' + str(x))

        # for x in range(coord[1]):
        #     for y in range(y_size):
        #         to_rem_from_queue.append(str(y) + ',' + str(x))

        # for to_rem in to_rem_from_queue:
        #     if to_rem in removed:
        #         continue
        #     removed.add(to_rem)
        #     queue.pop(to_rem)
        # removed.add(next_up[0])

        # look at all the neighbors for our current location (next_up)
        for neighbor, cost in map[next_up[0]].items():
            # we only care about locations still in the queue?
            if neighbor in queue:
                # 999999999 is our cheap representation of infinity, we need to add
                # up costs to get there so set to 0 if it's 'infinity'...
                cur_cost_to_neighbor = queue[neighbor]
                via_cur_loc_to_neighbor = next_up[1] + cost
                # if there is a current cost for the neighbor then we have already
                # found a path to get to it, and we need to compare it with this
                # new path we are currently checking to see which is cheaper
                if cur_cost_to_neighbor > via_cur_loc_to_neighbor:
                    # our new way of getting to the neighbor is cheaper than our
                    # already known path or we've not seen this neighbor before,
                    # update neighbor cost
                    queue[neighbor] = via_cur_loc_to_neighbor
                    # via[neighbor] = next_up[0]

        # resort the queue based on new data
        queue = sort_queue(queue)

    return finished[end_location]


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
