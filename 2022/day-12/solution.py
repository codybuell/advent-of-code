#!/usr/bin/env python3
# https://adventofcode.com/2022/day/12

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

################################################################################
##                                                                            ##
##  Generate Map & Metadata                                                   ##
##                                                                            ##
################################################################################

# .-------- Y -------->
# |
# |
# |
# X
# |
# |
# |
# V

# convert to 2d matrix with decimal values for easy storage
topo_map  = [[ord(letter) - 96 for letter in line] for line in lines]

# if S note start and set coord elevation a, if E note end set coord elevation z
for x, row in enumerate(topo_map):
    locs_found = 0
    if locs_found == 2:
        break
    for y, char in enumerate(row):
        if char == -13:
            start_loc = (x, y)
            topo_map[x][y] = 1
            locs_found += 1
        if char == -27:
            end_loc = (x, y)
            topo_map[x][y] = 26
            locs_found += 1
        if locs_found == 2:
            break

# width and height
topo_map_width  = len(topo_map[0])
topo_map_height = len(topo_map)

################################################################################
##                                                                            ##
##  Helpers                                                                   ##
##                                                                            ##
################################################################################


def sort_queue(queue: dict):
    return {k: v for k, v in sorted(queue.items(), key=lambda item: item[1], reverse=True)}


def orthogonal_coords(coord: tuple, matrix: list = topo_map, add_orig: bool = False) -> list:
    """
    Provides all orthogonal steps around a provided coordinate,
    constrained by the edges of the 2 dimensional matrix.
    """

    # set some ranges for edge detection
    x_range = len(matrix) - 1
    y_range = len(matrix[0]) - 1

    # define how far out from coord we want to check
    check_range = range(-1, 2)

    # grab rough list of orthogonal coordinates
    orthog_coords = []
    for x_offset in check_range:
        orthog_coords.append([min(x_range, max(0, coord[0] + x_offset)), coord[1]])
    for y_offset in check_range:
        orthog_coords.append([coord[0], min(y_range, max(0, coord[1] + y_offset))])

    # sort and deduplicate them
    orthog_coords.sort()
    orthog_coords = [list(x) for x in set(tuple(x) for x in orthog_coords)]

    # in case we dont want to return the provided coordinate in the list
    if not add_orig:
        orthog_coords.remove(list(coord))

    return orthog_coords


def breadth_first_search_shortest_path(graph: dict, start, end) -> list:
    """
    Returns shortest path from start to end location.
    """
    path_list      = [[start]]
    path_index     = 0
    previous_nodes = {start}
    if start == end:
        return path_list[0]
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # search goal node
        if end in next_nodes:
            current_path.append(end)
            return current_path
        # add new paths
        for next_node in next_nodes:
            if next_node not in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # continue to next path in list
        path_index += 1
    # no path is found
    return []


################################################################################
##                                                                            ##
##  Part 1 (Poorly implemented Dijkstra)                                      ##
##                                                                            ##
################################################################################


def part_1(start_loc: tuple, end_loc: tuple):
    # build dict of all positions with their relative step height to neighbors ordered low to high
    # {
    #     'location': {
    #        'orthog_loc': height_diff,
    #        ...
    #     (0,0): {(0,1): 1, (1,0): 1},
    #     (0,1): {(0,0): 1, (0,2): 6},
    adjacencies = {}
    for x in range(topo_map_height):
        for y in range(topo_map_width):
            location = (x, y)
            loc_val = topo_map[location[0]][location[1]]

            around = orthogonal_coords(location)
            values = [topo_map[p[0]][p[1]] for p in around]

            adjacencies[location] = {}

            # append to adjacencies IF
            # cost will always be one since were considering jumps and not step height
            # for idx, step in enumerate(around):
            #     adjacencies[location][tuple(step)] = values[idx] - loc_val
            for idx, step in enumerate(around):
                if (values[idx] - loc_val) <= 1:
                    adjacencies[location][tuple(step)] = 1

            # sort the entry by it's dict values
            # adjacencies[location] = {k: v for k, v in sorted(adjacencies[location].items(), key=lambda item: item[1])}

    # build a priority queue, some rough approximation of Dijkstra's algorithm
    # init everything with a high step except 0,0 our starting location
    # cost tracked in queue is cheapest cost to get to key from '0,0'
    queue = {k: 999999999 for k in adjacencies}
    queue[start_loc] = 0

    # just in case ensure we sort our queue by value (in reverse so we can popitem())
    queue = sort_queue(queue)

    # build a via dict to track how we got to each location
    via = {k: '' for k in adjacencies}

    # assign queue values to neighbors of our starting position and track how we got there
    for neighbor, cost in adjacencies[start_loc].items():
        queue[neighbor] = cost
        via[neighbor] = start_loc
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
        for neighbor, cost in adjacencies[next_up[0]].items():
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

    return finished[end_loc]


# print('part 1:', part_1(start_loc, end_loc))

################################################################################
##                                                                            ##
##  BRUUUTE FOOOORCE (3.5hr run time)                                         ##
##                                                                            ##
################################################################################


def part_2():
    # find all 1 value locations
    starts = {}
    for x, row in enumerate(topo_map):
        for y, char in enumerate(row):
            if char == 1:
                starts[(x, y)] = 999999

    for start in starts:
        starts[start] = part_1(start, end_loc)

    order = sort_queue(starts, )
    shortest = order.popitem()
    return shortest[1]


# print('part 2:', part_2())

################################################################################
##                                                                            ##
##  Rework (better implemented BFS)                                           ##
##                                                                            ##
################################################################################

# build out our graph
# {
#      coord: [list of possible orthogonal coords]
#     (x, y): [(x, y), (x, y)],
#     ...
graph = {}
for x in range(topo_map_height):
    for y in range(topo_map_width):
        # get details of location
        loc = (x, y)
        val = topo_map[loc[0]][loc[1]]
        around = orthogonal_coords(loc)
        values = [topo_map[p[0]][p[1]] for p in around]

        # append to our graph if we can step to it
        graph[loc] = []
        for idx, step in enumerate(around):
            if (values[idx] - val) <= 1:
                graph[loc].append(tuple(step))


print('part 1:', len(breadth_first_search_shortest_path(graph, start_loc, end_loc)) - 1)

# TODO: for an optimized part two rewrite bfs search but to stop when node equals a desired target value, not location, and then reverse your search from end location to the shortest value of 1...

starts = {}
for x, row in enumerate(topo_map):
    for y, char in enumerate(row):
        if char == 1:
            starts[(x, y)] = 999999

for start in starts:
    distance = len(breadth_first_search_shortest_path(graph, start, end_loc)) - 1
    if distance > 1:
        starts[start] = distance

order = {k: v for k, v in sorted(starts.items(), key=lambda item: item[1], reverse=True)}

shortest = order.popitem()
print('part 2:', shortest[1])
