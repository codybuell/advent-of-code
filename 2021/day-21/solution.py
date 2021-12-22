#!/usr/bin/env python
# https://adventofcode.com/2021/day/21

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
player_1 = int(lines[0].replace('Player 1 starting position: ', ''))
player_2 = int(lines[1].replace('Player 2 starting position: ', ''))

# for part two, sums from quantum roles and their number of occurrences, don't
# care about the realities they split into, just their result and how many
# times they would have occurred, allows us to math it out instead of brute
# force a few 100 trillion iterations...
occurrences = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


###########
#  funcs  #
###########


def play_game(positions: list, scores: list, player: int, wins: list, multiple: int) -> list:
    """ Play game from provided state and return the winner counts as a list. """

    # start tracking some items for this universe configuraion
    wincount = 0
    to_recurse = []

    # a combination of rolls has occurred, universes split, multiple times but
    # they end up in the states described in occurrences (27 universes result,
    # sums range from 3 to 9), iterate through each resulting condition rather
    # than each resulting universe
    for sum, count in occurrences.items():
        # each iteration of this loop represents a new universe configuration
        # so split the state by copying the vars so they modify independently
        positions_x = positions.copy()
        scores_x    = scores.copy()
        wins_x      = wins.copy()

        # update the current players position
        for i in range(sum):
            positions_x[player] += 1
            # loop back round to 1 after 10
            if positions_x[player] > 10:
                positions_x[player] = 1

        # update the current player score
        scores_x[player] += positions_x[player]

        # derive a new multiple based on how many occurrences of this current
        # universe exist and how many of the derived roll exist
        count *= multiple

        # if we have a winner
        if scores_x[player] >= 21:
            # add to wincount, this win counts count times times current wins
            wincount += count
        else:
            # switch players
            next_player = 0 if player == 1 else 1
            # capture the next state to recurse into later, and how many multiples would be derived
            to_recurse.append((positions_x, scores_x, next_player, wins_x, count))

    # count our wins for this go of things
    wins[player] += wincount

    # now recurse into every state that did not result in a win
    if len(to_recurse):
        for conditions in to_recurse:
            wins_to_append = play_game(*conditions)
            wins[0] += wins_to_append[0]
            wins[1] += wins_to_append[1]

    return wins


###########
#  parts  #
###########


def part1():
    # setup initial state
    die       = 1
    rolls     = 0
    player    = 0
    round     = 1
    scores    = [0, 0]
    positions = [player_1, player_2]

    # keep playing until end condition
    while True:
        # sum up next three rolls
        sum = 0
        for i in range(3):
            # loop back round to 1 after 100
            if die > 100:
                die = 1
            # track our roll
            sum   += die
            die   += 1
            rolls += 1

        # lazy loop around our the board
        for i in range(sum):
            positions[player] += 1
            # loop back round to 1 after 10
            if positions[player] > 10:
                positions[player] = 1

        # update game state
        scores[player] += positions[player]
        player = round % 2
        round += 1

        # check for end condition
        if scores[0] >= 1000 or scores[1] >= 1000:
            break

    return min(scores) * rolls


def part2():
    # setup initial state
    scores       = [0, 0]
    positions    = [player_1, player_2]
    start_player = 0
    wins         = [0, 0]
    multiple     = 1

    return max(play_game(positions, scores, start_player, wins, multiple))


##########
#  main  #
##########


if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
