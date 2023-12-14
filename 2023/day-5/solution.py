#!/usr/bin/env python3
# https://adventofcode.com/2023/day/5

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# grab our seeds
seeds = [int(x) for x in lines.pop(0).replace('seeds: ', '').split()]

# restructure maps into a list of lists for each map
lines.pop(0)
raw_maps  = []
temp_list = []
for line in lines:
    if line == '':
        raw_maps.append(temp_list)
        temp_list = []
    else:
        temp_list.append(line)
raw_maps.append(temp_list)

# parse the maps
maps = {}
for map in raw_maps:
    map_name = map.pop(0).replace(' map:', '')
    maps[map_name] = []
    for chunk in map:
        nums = chunk.split()
        maps[map_name].append({
            'dest_start':   int(nums[0]),
            'source_start': int(nums[1]),
            'range_len':    int(nums[2]),
            'offset': int(nums[0]) - int(nums[1])
        })


def chunk_it(to_map: str, input: int) -> int:
    for map in maps[to_map]:
        if input >= map['source_start'] and input <= map['source_start'] + map['range_len']:
            return input + map['offset']
    return input


# part 1
locs = []
for seed in seeds:
    # print('seed', seed, 'to soil', maps['seed-to-soil'].get(seed) or seed)
    soil = chunk_it('seed-to-soil', seed)
    fert = chunk_it('soil-to-fertilizer', soil)
    watr = chunk_it('fertilizer-to-water', fert)
    lite = chunk_it('water-to-light', watr)
    temp = chunk_it('light-to-temperature', lite)
    humd = chunk_it('temperature-to-humidity', temp)
    loc  = chunk_it('humidity-to-location', humd)
    locs.append(loc)

print('Part 1:', min(locs))

# part 2 (slooooooow, 3.5hrs)
minn = 99999999999999999999999999999999999999999
while len(seeds):
    start = seeds.pop(0)
    length = seeds.pop(0)
    for seed in range(start, start + length):
        # print('seed', seed, 'to soil', maps['seed-to-soil'].get(seed) or seed)
        soil = chunk_it('seed-to-soil', seed)
        fert = chunk_it('soil-to-fertilizer', soil)
        watr = chunk_it('fertilizer-to-water', fert)
        lite = chunk_it('water-to-light', watr)
        temp = chunk_it('light-to-temperature', lite)
        humd = chunk_it('temperature-to-humidity', temp)
        loc  = chunk_it('humidity-to-location', humd)
        minn = min(minn, loc)

print('Part 2:', minn)
