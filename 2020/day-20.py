#!/usr/bin/env python3
# https://adventofcode.com/2020/day/20

import re
import sys

dataFile = open('day-20.txt', 'r')
data     = dataFile.read().split('\n\n')

class Tile():

    def __init__(self, raw):
        raw = raw.splitlines()

        # id and the tile with borders
        self.id  = int(raw[0].replace('Tile ','').replace(':',''))
        self.raw = raw[1:]

        # matches (0->top, 1->right, 2->bottom, 3->left) { 0: id, 1: id, 2: id, 3: id }
        self.matches = {0:'',1:'',2:'',3:''}

        # list of id's compared against
        self.compared = []

    def show(self):
        for l in self.raw:
            print(l)

    def matching_sides(self):
        count = 0
        for k, v in self.matches.items():
            if v != '':
                count += 1
        return count

    def top(self):
        return self.raw[0]

    def right(self):
        return ''.join([r[-1] for r in self.raw])

    def bottom(self):
        return self.raw[-1]

    def left(self):
        return ''.join([r[0] for r in self.raw])

    def sides(self):
        return [self.top(), self.right(), self.bottom(), self.left()]

    def sides_flipped(self):
        return [self.top()[::-1], self.right()[::-1], self.bottom()[::-1], self.left()[::-1]]

    def borderless(self):
        return [x[1:-1] for x in self.raw[1:-1]]

    def r1(self):
        # turn into a matrix
        matrix = []
        for i in self.raw:
            matrix.append(list(i))

        # perform one clockwise rotation on matrix
        N = len(matrix[0])
        for i in range(N // 2):
            for j in range(i, N - i - 1):
                temp = matrix[i][j]
                matrix[i][j] = matrix[N - 1 - j][i]
                matrix[N - 1 - j][i] = matrix[N - 1 - i][N - 1 - j]
                matrix[N - 1 - i][N - 1 - j] = matrix[j][N - 1 - i]
                matrix[j][N - 1 - i] = temp

        # write back over raw
        for idx, i in enumerate(matrix):
            self.raw[idx] = ''.join(i)

        # rotate matches
        topmatch    = self.matches[0]
        rightmatch  = self.matches[1]
        bottommatch = self.matches[2]
        leftmatch   = self.matches[3]
        self.matches[0] = leftmatch
        self.matches[1] = topmatch
        self.matches[2] = rightmatch
        self.matches[3] = bottommatch

    def rotate(self, count=1):
        for i in range(count):
            self.r1()

    def flip(self):
        # flip once on around horizontal axis ^v
        self.raw = self.raw[::-1]
        topmatch    = self.matches[0]
        bottommatch = self.matches[2]
        self.matches[0] = bottommatch
        self.matches[2] = topmatch

def part1():
    # init our objects
    tiles = {}
    for tile in data:
        t = Tile(tile)
        tiles[t.id] = t

    # check for matches as oriented
    for tid1, t1 in tiles.items():
        for tid2, t2 in tiles.items():
            # skip if we've compared before or checking self
            if tid1 == tid2 or tid1 in t2.compared:
                continue

            # track that we've compared
            t1.compared.append(tid2)
            t2.compared.append(tid1)

            # check for matching sides as oriented
            matches = set(t1.sides()) & set(t2.sides())
            for match in matches:
                t1index = t1.sides().index(match)
                t2index = t2.sides().index(match)
                t1.matches[t1index] = str(t2.id) + ':' + str(t2index)
                t2.matches[t2index] = str(t1.id) + ':' + str(t1index)

            # check for matches as flipped (only need to flip one)
            matches_flipped = set(t1.sides_flipped()) & set(t2.sides())
            for match in matches_flipped:
                t1index = t1.sides_flipped().index(match)
                t2index = t2.sides().index(match)
                t1.matches[t1index] = str(t2.id) + ':' + str(t2index)
                t2.matches[t2index] = str(t1.id) + ':' + str(t1index)

    # multiply all corner id's together
    prod = 1
    for tid, t in tiles.items():
        # if only two sides have matches it's a corner
        # if only three sides have matches it's a side
        # if four sides have matches it's an inner
        # if zero or one sides have a match its a bad tile
        if t.matching_sides() == 2:
            prod *= tid

    return tiles, prod

def part2(tiles):
    # track assembly [y][x] and current location
    assembly   = [[]]
    location_y = 0
    location_x = 0

    # find a corner piece and log it in assembly[0][0]
    for tid, t in tiles.items():
        if t.matching_sides() ==  2:
            starting_piece = tid
            break
    assembly[0].append(starting_piece)

    # re-orient to be top left [0][0], rotate till sides with matches are right and bottom
    while True:
        if tiles[starting_piece].matches[0] == '' and tiles[starting_piece].matches[3] == '':
            break
        tiles[starting_piece].rotate()

    # assemble left to right top to bottom
    while True:
        # build out to the right, flipping and rotating as needed
        while True:
            current_piece_id   = assembly[location_y][location_x]
            current_right_side = tiles[current_piece_id].right()
            next_piece         = tiles[current_piece_id].matches[1]

            # if there is no right piece we've reached the end break
            if next_piece == '':
                break

            # get info on next piece
            next_piece_id   = int(next_piece.split(':')[0])
            next_piece_side = int(next_piece.split(':')[1])

            # note it in our assembly matrix
            assembly[location_y].append(next_piece_id)

            # rotate till our matching side is on the left
            rotations = 3 - next_piece_side
            tiles[next_piece_id].rotate(rotations)

            # check alignment, flip if needed (no rotation required)
            if tiles[next_piece_id].left() != current_right_side:
                tiles[next_piece_id].flip()

            # increment along x
            location_x += 1

        # go back to the beginning of the row and get x=0's bottom tile match
        next_row_starter = tiles[assembly[location_y][0]].matches[2]
        if next_row_starter == '':
            break

        # else go down one row
        location_y += 1
        location_x  = 0
        assembly.append([])

        # find the match for it, log it in assembly
        next_row_starter_id   = int(next_row_starter.split(':')[0])
        next_row_starter_side = int(next_row_starter.split(':')[1])
        assembly[location_y].append(next_row_starter_id)

        # rotate till our matching side is on the top
        if next_row_starter_side != 0:
            rotations = 4 - next_row_starter_side
            tiles[next_row_starter_id].rotate(rotations)

        # if it doesn't fit with the piece above, flip and rotate if needed
        if tiles[next_row_starter_id].top() != tiles[assembly[location_y - 1][0]].bottom():
            tiles[next_row_starter_id].flip()
            tiles[next_row_starter_id].rotate(2)

    # generate image from current assembly
    image = assemble_image(tiles, assembly)

    # check each orientation until we find sea monsters
    rotations = 0
    flipped   = False
    while True:
        # stop after we have checked 4 rotations on each side
        if rotations == 3 and flipped:
            break

        # count seamonsters
        hashes, monsters = identify_seamonsters(image)

        if monsters:
            print(hashes)
            break
        # if no monsters and we have rotated 4 times but not flipped, flip it
        elif rotations == 3 and not flipped:
            image = image[::-1]
            rotations = 0
        # if we have no monsters and 
        else:
            image = rotate_image(image)
            rotations += 1

def assemble_image(tiles, assembly):
    image       = []
    tile_height = len(tiles[assembly[0][0]].borderless())
    row         = 0
    for assembly_row in assembly:
        for h in range(tile_height):
            image.append('')
            for tile_id in assembly_row:
                image[row] += tiles[tile_id].borderless()[h]
            row += 1

    return image

def identify_seamonsters(image):
    # our monster patern in binary
    monster = [
            '00000000000000000010',
            '10000110000110000111',
            '01001001001001001000'
            ]

    # build out indexes of body bits
    body_index = [[],[],[]]
    for idxr, r in enumerate(monster):
        for idx, c in enumerate(r):
            if c == '1':
                body_index[idxr].append(idx)

    # measurements
    monster_height = len(monster)
    monster_width  = len(monster[0])
    image_height   = len(image)
    image_width    = len(image[0])
    monster_count  = 0
    hash_count     = 0

    # make a new image to mark with sea monster locations
    flagged_image = image.copy()

    # walk our image starting at [0][0] stop when monster wounld overflow right side or bottom of image
    for y_start in range(image_height - monster_height + 1):
        for x_start in range(image_width - monster_width + 1):
            # for our frame convert image to binary, do a bitwise and with monster, match
            # will show overlap of the image frame we are looking at with the monster shape
            match = []
            for i in range(monster_height):
                y = image[y_start + i][x_start:monster_width + x_start]
                ybin = y.replace('.','0').replace('#','1')
                match.append(format(int(ybin, 2) & int(monster[i], 2), '0' + str(monster_width) + 'b'))
            # if our match looks exactly like our monster we found a monster, flag the body locations in flagged_image
            if match == monster:
                monster_count += 1
                for i in range(monster_height):
                    row = y_start + i
                    for b in body_index[i]:
                        img = flagged_image[row]
                        flagged_image[row] = img[:b + x_start] + 'O' + img[b + x_start + 1:]

    # count up turbulent waters (#'s) if we saw monsters
    if monster_count:
        for i in flagged_image:
            print(i)
            hash_count += i.count('#')

    return hash_count, monster_count

def rotate_image(image):
    rotated_image = []

    # pop first col from each row into a new string, reverse that, append to rotated image
    for i in range(len(image[0])):
        col = ''
        for row in image:
            col += row[i]
        rotated_image.append(col[::-1])

    return rotated_image

if __name__ == "__main__":
    tiles, prod = part1()
    print(prod)
    part2(tiles)
