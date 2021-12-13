#!/usr/bin/env python
# https://adventofcode.com/2021/day/12


import copy


###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
data = [line.split('-') for line in dataFile.read().splitlines()]

# build an adjacency dictionary
adjacency_dict = {}
for line in data:
    for position in line:
        if position not in adjacency_dict:
            adjacency_dict[position] = set()

    adjacency_dict[line[0]].add(line[1])
    adjacency_dict[line[1]].add(line[0])

# convert our sets to lists for ease of use
adjacency_dict = {k: list(v) for (k, v) in adjacency_dict.items()}


###########
#  funcs  #
###########


def find_possible_paths(possible_paths: list, options: list, complete_paths: list):
    for path in possible_paths:
        # determine what cave we need to tie together
        last_connector = path[-1]

        # find what options match that cave
        can_connect = []
        for option in options:
            if option[0] == last_connector:
                can_connect.append(option)

        # id all the lowercase caves in our path, excluding last and start
        visited_small = [x for x in path[0:-1] if x.islower() and x != 'start']

        # id all options that tie into our path
        can_connect = [x for x in options if x[0] == last_connector]

        # remove options that contain an already visited small cave
        to_connect = [x for x in can_connect if not any(i in x for i in visited_small)]

        # build out new possible paths from current path
        new_paths = []
        for addon in to_connect:
            path_copy = path.copy()
            path_copy.append(addon[-1])
            new_paths.append(path_copy)

        # identify complete paths
        complete_paths.extend([x for x in new_paths if x[-1] == 'end'])

        # identify incomplete paths
        incomplete_paths = [x for x in new_paths if x[-1] != 'end']

        # keep going if we have any incomplete paths
        if len(incomplete_paths):
            find_possible_paths(incomplete_paths, options, complete_paths)

    return complete_paths


def print_adjacency_dict(adj: dict):
    print('')
    print('*** Adjacency Dictionary ***')
    for entry in adj:
        print(entry, adj[entry])
    print('*** -------------------- ***')
    print('')


def find_paths_pt1(paths: list, adj_dict: dict, complete_paths: list) -> list:
    """ Returns a list of possible paths. """
    for path in paths:
        # grab where we are in the path
        current_cave = path[-1]

        # grab all small caves we've visited
        visited_small = [x for x in path[0:-1] if x.islower() and x != 'start']

        # determine what caves we need to visit (adjacentcies - visited_small)
        to_visit = [x for x in adj_dict[current_cave] if x not in visited_small]

        # build out new possible paths from current path
        new_paths = []
        for cave in to_visit:
            path_copy = path.copy()
            path_copy.append(cave)
            new_paths.append(path_copy)

        # id complete paths
        complete_paths.extend([x for x in new_paths if x[-1] == 'end'])

        # identify incomplete paths
        incomplete_paths = [x for x in new_paths if x[-1] != 'end']

        # keep going if we have any incomplete paths
        if len(incomplete_paths):
            find_paths_pt1(incomplete_paths, adj_dict, complete_paths)

    return complete_paths


def find_paths_pt2(paths: list, adj_dict: dict, complete_paths: list) -> list:
    """ Returns a list of possible paths. """
    for path in paths:
        # grab where we are in the path
        current_cave = path[-1]

        # grab all small caves we've visited
        visited_small = [x for x in path if x.islower() and x != 'start']

        # id small caves we've visited more than once and remove it from adjacency dict targets
        visited_a_small_twice = False
        if len(visited_small) >= 2:
            for cave in visited_small:
                if visited_small.count(cave) == 2:
                    visited_a_small_twice = True
                    break

        # determine what caves we need to visit conditionally (adjacentcies - visited_small)
        if visited_a_small_twice:
            to_visit = [x for x in adj_dict[current_cave] if x not in visited_small]
        else:
            to_visit = adj_dict[current_cave]

        # build out new possible paths from current path
        new_paths = []
        for cave in to_visit:
            path_copy = path.copy()
            path_copy.append(cave)
            new_paths.append(path_copy)

        # id complete paths
        complete_paths.extend([x for x in new_paths if x[-1] == 'end'])

        # identify incomplete paths
        incomplete_paths = [x for x in new_paths if x[-1] != 'end']

        # print("path:            ", path)
        # print("current cave:    ", current_cave)
        # print("visited small:   ", visited_small)
        # print("visited sm twice:", visited_a_small_twice)
        # print("to_visit:        ", to_visit)
        # print("complete paths:  ", complete_paths)
        # print("incomplete pths: ", incomplete_paths)

        # print('---')

        # input()

        # keep going if we have any incomplete paths
        if len(incomplete_paths):
            find_paths_pt2(incomplete_paths, adj_dict, complete_paths)

    return complete_paths


###########
#  parts  #
###########


def part1():
    # # this approach seems to find only direct routes, no bouncing into side caves,
    # # works only with example data... where data is structured with start in first pos
    # starts  = [x for x in data if x[0] == 'start']
    # options = [x for x in data if x[0] != 'start']
    # complete_paths = find_possible_paths(starts, options, [])
    # for path in complete_paths:
    #     print(path)

    # remove any entries from adjacency dict that are lowercase and only
    # contain lowercase entries, these constitute invalid moves since you can
    # only visit lowercase places once
    pt1_adj_dict = copy.deepcopy(adjacency_dict)
    to_remove = []
    for k, v in pt1_adj_dict.items():
        if k.islower() and len(v) == 1 and v[0].islower():
            to_remove.append(k)
    for key in to_remove:
        pt1_adj_dict.pop(key)

    # now remove start and removed positions from adjacencies as they cannot be visited
    to_remove.append('start')
    for key in pt1_adj_dict:
        pt1_adj_dict[key] = [pos for pos in pt1_adj_dict[key] if pos not in to_remove]

    # print_adjacency_dict(pt1_adj_dict)

    # start our paths from starting position
    paths = [['start', x] for x in pt1_adj_dict['start']]

    # build out path posibilities
    complete_paths = find_paths_pt1(paths, pt1_adj_dict, [])

    # for path in complete_paths:
    #     print(path)

    return len(complete_paths)


def part2():
    # remove start from available target caves
    for key in adjacency_dict:
        adjacency_dict[key] = [pos for pos in adjacency_dict[key] if pos != 'start']

    # start our paths from starting position
    paths = [['start', x] for x in adjacency_dict['start']]

    # print_adjacency_dict(adjacency_dict)

    # build out path posibilities
    complete_paths = find_paths_pt2(paths, adjacency_dict, [])

    # for path in complete_paths:
    #     print(path)

    return len(complete_paths)


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
