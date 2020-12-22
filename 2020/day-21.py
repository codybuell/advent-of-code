#!/usr/bin/env python3
# https://adventofcode.com/2020/day/21

import re
import sys

dataFile  = open('day-21.txt', 'r')
food_list = dataFile.read().splitlines()

def part1():
    # build a list of possible values for each allergen by bitwise &-ing sets of foods
    allergen_list   = {}
    all_ingredients = set()
    parsed_list     = {}
    foods_parsed    = []
    p = '(^[^(]*) \(contains ([^)]*)\)$'
    for food in food_list:
        m = re.match(p, food)
        allergens = m.group(2).split(', ')
        foods     = m.group(1).split(' ')
        foods_parsed.append(foods)
        for a in allergens:
            # if we have foods listed for the allergen, merge sets
            if a in allergen_list:
                allergen_list[a] = list(set(allergen_list[a]) & set(foods))
            # else add a new set of the foods
            else:
                allergen_list[a] = foods
        for f in foods:
            all_ingredients.add(f)

    # now look through our allergen_list and find a known allergen, one that
    # has only one associated food, and set it on our final list, remove it
    # from all other allergen list sets and repeat
    allergen_ingredient_map = {}
    while len(allergen_ingredient_map) != len(allergen_list):
        for allergen, foods in allergen_list.items():
            if len(foods) == 1:
                allergen_ingredient_map[allergen] = foods[0]
                for a2, f2 in allergen_list.items():
                    if allergen != a2 and foods[0] in f2:
                        f2.remove(foods[0])

    # build list of ingredients with allergens
    ingredients_with_allergens = set()
    for allergen, food in allergen_ingredient_map.items():
        ingredients_with_allergens.add(food)

    # identify allergen free foods
    allergen_free_ingredients = all_ingredients.copy()
    for food in ingredients_with_allergens:
        allergen_free_ingredients.remove(food)

    # count how many times allergen free foods show up in food_list
    count = 0
    for ingredient in allergen_free_ingredients:
        for food in foods_parsed:
            count += food.count(ingredient)

    print(count)
    return allergen_ingredient_map

def part2(allergen_map):
    ordered_ingredients = []
    for allergen in sorted(allergen_map):
        ordered_ingredients.append(allergen_map[allergen])

    print(','.join(ordered_ingredients))

if __name__ == "__main__":
    allergen_map = part1()
    part2(allergen_map)
