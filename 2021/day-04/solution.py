#!/usr/bin/env python
# https://adventofcode.com/2021/day/4

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
numbers = lines[0].split(',')
numbers = [int(x) for x in numbers]
boards  = [[]]
board_count = 0
for line in lines[2:]:
    if line != '':
        entries = line.split()
        entries = [int(x) for x in entries]
        boards[board_count].append(entries)
    else:
        boards.append([])
        board_count += 1


###########
#  funcs  #
###########


def check_board(numbers: list, board: list) -> bool:
    # check horizontals
    for y in board:
        winner = True
        for val in y:
            if val not in numbers:
                winner = False
        if winner:
            return winner

    # check verticals
    for x in range(len(board[0])):
        winner = True
        for y in board:
            if y[x] not in numbers:
                winner = False
        if winner:
            return winner

    return winner


###########
#  parts  #
###########


def part1():
    # find the first winning board and winning number
    winner = False
    for inum, num in enumerate(numbers):
        if not winner:
            for board in boards:
                if check_board(numbers[:inum + 1], board):
                    called_numbers = numbers[:inum + 1]
                    winning_board = board
                    winning_number = num
                    winner = True
                    break

    # sum up all unmarked numbers
    sum = 0
    for y in winning_board:
        for val in y:
            if val not in called_numbers:
                sum += val

    # multiply winning number by the sum
    print(sum * winning_number)


def part2():
    winning_boards = []
    for inum, num in enumerate(numbers):
        for iboard, board in enumerate(boards):
            if iboard in winning_boards:
                continue
            if check_board(numbers[:inum + 1], board):
                sum = 0
                for y in board:
                    for val in y:
                        if val not in numbers[:inum + 1]:
                            sum += val
                print("board", iboard, "wins with a score of", sum * num)
                winning_boards.append(iboard)


##########
#  main  #
##########


if __name__ == "__main__":
    part1()
    print('---')
    part2()
