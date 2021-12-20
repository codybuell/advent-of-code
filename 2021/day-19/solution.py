#!/usr/bin/env python
# https://adventofcode.com/2021/day/19

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform into a list of scanners
scanners = []
idx = -1
for line in lines:
    if line.startswith("---"):
        scanners.append([])
        idx += 1
    elif line:
        scanners[idx].append(tuple(int(x) for x in line.split(',')))


###########
#  funcs  #
###########


def get_distance_btw(a: list, b: list) -> float:
    """ Determine exact distance between two points in a 3d matrix. """
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    z1 = a[2]
    z2 = b[2]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** (1 / 2)


def generate_fingerprints(beacons: list) -> list:
    """ For each beacon in list make a sublist of distances to every other beacon. """
    fingerprints = []
    for beacon_a in beacons:
        new_beacon_bits = []
        for beacon_b in beacons:
            distance = get_distance_btw(beacon_a, beacon_b)
            new_beacon_bits.append(abs(distance))
        fingerprints.append(new_beacon_bits)
    return fingerprints


def get_vector(a: list, b: list) -> list:
    """ Get vector between two points, is this a derivaton? """
    x = a[0] - b[0]
    y = a[1] - b[1]
    z = a[2] - b[2]
    return [x, y, z], [abs(x), abs(y), abs(z)]


###########
#  parts  #
###########


def main():
    # start our scanner map with scanner 0
    scanner_map = scanners.pop(0)
    scanner_positions = [(0, 0, 0)]

    # repeat until we have no more scanners to work with
    while len(scanners):
        # generate a fingerprint for our scanner map
        map_fingerprint = generate_fingerprints(scanner_map)

        # loop through remaining scanners to fing a match
        for idx, scanner in enumerate(scanners):
            # generate a fingerprint for our scanner
            scanner_fingerprint = generate_fingerprints(scanner)

            # compare beacons between scanner_map and scanner, track aligned beacons
            aligned_beacons = []
            for idx_a, fp_a in enumerate(map_fingerprint):
                for idx_b, fp_b in enumerate(scanner_fingerprint):
                    beacons_same_distance = len([x for x in fp_b if x in fp_a])
                    if beacons_same_distance >= 12:
                        # track the index of corresponding beacons within each scanner
                        aligned_beacons.append([idx_a, idx_b])
                        # print(scanner_map[idx_a], '\t', scanner[idx_b])

            # if we have at least 12 aligned beacons then its a match
            if len(aligned_beacons) >= 12:
                # remove the scanner from our scanners list
                matched_scanner = scanners.pop(idx)

                # get the same two points from scanner_map and matched_scanner
                beacon_a = [scanner_map[aligned_beacons[0][0]], matched_scanner[aligned_beacons[0][1]]]
                beacon_b = [scanner_map[aligned_beacons[1][0]], matched_scanner[aligned_beacons[1][1]]]

                # get vectors for each pair to see how we need to manipulate the matched scanner
                va = get_vector(beacon_a[0], beacon_b[0])      # scanner map vector
                vb = get_vector(beacon_a[1], beacon_b[1])      # matched scanner vector

                # determine index of x, y, and z in matched scanner by looking
                # at absolute valuees of vectors, if our vectors don't match
                # then it's not an actual overlap, put match back on the end of
                # scanners and try again
                try:
                    bx = vb[1].index(va[1][0])
                    by = vb[1].index(va[1][1])
                    bz = vb[1].index(va[1][2])
                except ValueError:
                    scanners.append(matched_scanner)
                    continue

                # determine what inversions are needed
                inv_x = 1 if va[0][0] == vb[0][bx] else -1
                inv_y = 1 if va[0][1] == vb[0][by] else -1
                inv_z = 1 if va[0][2] == vb[0][bz] else -1

                # determine the scanner location of matched_scanner based on
                # distances of each from a normalized beacon a
                diff_x = beacon_a[0][0] - (beacon_a[1][bx] * inv_x)
                diff_y = beacon_a[0][1] - (beacon_a[1][by] * inv_y)
                diff_z = beacon_a[0][2] - (beacon_a[1][bz] * inv_z)

                # capture the matched scanners location
                matched_scanner_loc = [diff_x, diff_y, diff_z]
                scanner_positions.append(tuple(matched_scanner_loc))

                # apply transformation to all beacons in matched scanner
                transformed_beacons = []
                for beacon in matched_scanner:
                    flipped = [beacon[bx] * inv_x, beacon[by] * inv_y, beacon[bz] * inv_z]
                    transformed_beacons.append(tuple([
                        matched_scanner_loc[0] + flipped[0],
                        matched_scanner_loc[1] + flipped[1],
                        matched_scanner_loc[2] + flipped[2],
                    ]))

                scanner_map.extend(transformed_beacons)
                scanner_map = [t for t in (set(tuple(i) for i in scanner_map))]

    print('Part 1:', len(scanner_map))

    # build a list of unique scanner combinations to compare
    distances = []
    for i in range(len(scanner_positions)):
        for j in range(i, len(scanner_positions)):
            if i != j:
                a = scanner_positions[i]
                b = scanner_positions[j]
                distances.append(abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]))

    print('Part 2:', max(distances))


##########
#  main  #
##########


if __name__ == "__main__":
    main()
