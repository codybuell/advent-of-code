#!/usr/bin/env python3
# https://adventofcode.com/2024/day/4

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

data = [[x for x in line] for line in lines]

word = 'XMAS'

length    = len(word)
forwards  = word
backwards = word[::-1]
found     = 0


def check(input, forwards, backwards) -> int:
    count = 0

    for row in input:
        for i in range(len(row) - len(forwards) + 1):
            checking = ''.join(row[i:i + length])
            if forwards == checking:
                count += 1
            if backwards == checking:
                count += 1

    return count


def rotate_45_cw(matrix) -> list:
    n = len(matrix)
    m = len(matrix[0])
    diagonal = []

    for i in range(n):
        for j in range(m):
            new_index = i + j
            if new_index >= len(diagonal):
                diagonal.append([])
            diagonal[new_index].append(matrix[i][j])

    return diagonal


# count horizontal
found += check(data, forwards, backwards)

# transform the data so we can check vertical and diagonal
horizontal = list(zip(*data))

# count vertical
found += check(horizontal, forwards, backwards)

# count diagonal
found += check(rotate_45_cw(data), forwards, backwards)

# now the other diagonal
found += check(rotate_45_cw([row[::-1] for row in data]), forwards, backwards)

print(found)

# make 3 x 3 matrices
n = len(data)
m = len(data[0])
submatrices = []

for i in range(n - 2):
    for j in range(m - 2):
        submatrix = [row[j:j + 3] for row in data[i:i + 3]]
        submatrices.append(submatrix)

# for each 3 x 3 check diagonals, if > 1 then we have a match
found = 0
for submatrix in submatrices:
    count  = check(rotate_45_cw(submatrix), 'MAS', 'SAM')
    count += check(rotate_45_cw([row[::-1] for row in submatrix]), 'MAS', 'SAM')
    if count > 1:
        found += 1

print(found)
