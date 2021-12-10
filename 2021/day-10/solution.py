#!/usr/bin/env python
# https://adventofcode.com/2021/day/10

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# define chunk types
chunk_types = ['()', '[]', '{}', '<>']

# placeholder for our incomplete lines
incomplete_lines = []


###########
#  funcs  #
###########


def reduce_pairs(line: str) -> str:
    while True:
        start_len = len(line)
        for chunk in chunk_types:
            line = line.replace(chunk, '')
        if len(line) == start_len:
            break
    return line


###########
#  parts  #
###########


def part1():
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    score = 0

    for line in lines:
        # capture the unedited line
        orig_line = line

        # remove all matching bracket until they cant be removed anymore
        line = reduce_pairs(line)

        # find lines that contain ]})>, those are corrupted, rest are incomplete
        for i in "<{([":
            line = line.replace(i, '')
        if len(line):
            # corrupted lines
            score += points[line[0]]
        else:
            # incomplete lines
            incomplete_lines.append(orig_line)

    return score


def part2():
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    scores = []

    for line in incomplete_lines:
        # reduce matching pairs, we are left with unmatched brackets
        line = reduce_pairs(line)

        # reverse the line and replace to derive our closing bracket pattern
        line = line[::-1]
        line = line.replace("{", "}")
        line = line.replace("(", ")")
        line = line.replace("[", "]")
        line = line.replace("<", ">")

        total_score = 0

        for i in line:
            total_score = (total_score * 5) + points[i]

        scores.append(total_score)

    scores.sort()
    return scores[len(scores) // 2]


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
