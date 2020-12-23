#!/usr/bin/env python3
# https://adventofcode.com/2020/day/22

import re
import sys

dataFile    = open('day-22.txt', 'r')
players_raw = dataFile.read().split('\n\n')

def assemble_hands():
    # assemble our starting hands
    starting_hands = []
    for player in players_raw:
        data = player.splitlines()
        starting_hands.append([int(c) for c in data[1:]])

    return starting_hands

def score_game(hand):
    # tally up the score per rules
    sum = 0
    for idx, c in enumerate(hand[::-1]):
        sum += (idx + 1) * c

    print(sum)

def part1():
    # build the players hands
    hands = assemble_hands()

    # play the game
    while True:
        # check if the game is over
        handsizes = [len(h) for h in hands]
        if 0 in handsizes:
            break

        # play the round
        draw    = [c.pop(0) for c in hands]    # get cards to compare
        ordered = sorted(draw, reverse=True)   # sort them
        winner  = draw.index(ordered[0])       # determine who is the winner
        hands[winner].extend(ordered)          # add the cards to their hand

    # determine the winner
    for idx, hand in enumerate(hands):
        if len(hand) > 0:
            winning_index = idx
            winning_hand  = hand

    score_game(winning_hand)

def part2():

    # define the game so we can recurse
    def game(hands):
        game_states = set()    # initialize hand history for this game

        # play rounds
        while True:
            # if one player has all the cards game is over, return winner and hands
            handsizes = [len(h) for h in hands]
            if 0 in handsizes:
                game_winner = 1 - handsizes.index(0)
                break

            # if we've seeen the hands before, player 0 wins by default, else track hands
            if (state := (tuple(hands[0]), tuple(hands[1]))) in game_states:
                game_winner = 0
                break
            game_states.add(state)

            # play the round
            draw       = [c.pop(0) for c in hands]    # get cards to compare
            hand_sizes = [len(h) for h in hands]      # get hand sizes after draw

            # if both have as many cards left in hand as the value of their drawn cards
            if draw[0] <= hand_sizes[0] and draw[1] <= hand_sizes[1]:
                # play a sub game, each player getting cards = their draw value
                round_winner,_ = game([hands[0][:draw[0]], hands[1][:draw[1]]])
                if round_winner == 0:
                    spoils = draw
                else:
                    spoils = draw[::-1]
            else:
                spoils  = sorted(draw, reverse=True)  # sort them
                round_winner  = draw.index(spoils[0]) # determine who is the winner

            hands[round_winner].extend(spoils)        # add the cards to their hand

        return game_winner, hands

    final_winner, hands = game(assemble_hands())
    score_game(hands[final_winner])

if __name__ == "__main__":
    part1()
    part2()
