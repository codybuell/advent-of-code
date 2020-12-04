#!/usr/bin/env python3
# https://adventofcode.com/2020/day/4

import re
import ast

dataFile  = open('day-04.txt', 'r')
passports = dataFile.read().split("\n\n")

passportStructure = {
    "byr": "Birth Year",
    "iyr": "Issue Year",
    "eyr": "Expiration Year",
    "hgt": "Height",
    "hcl": "Hair Color",
    "ecl": "Eye Color",
    "pid": "Passport ID",
    "cid": "Country ID"
}

validEyeColors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def parsePassports():

    parsedPassports = []

    for passport in passports:
        # strip any blank end lines
        passport = re.sub(r'\n$', '', passport)
        # replace spaces with new lines, put each value on a line
        passport = re.sub(r' ', '\n', passport)
        # then wrestle it into json / dictionary format
        passport = re.sub(r'^', '{"', passport) 
        passport = re.sub(r':', '":"', passport) 
        passport = re.sub(r'\n', '","', passport) 
        passport = re.sub(r'$', '"}', passport) 

        # convert our string to a dictionary
        parsedPassports.append(ast.literal_eval(passport))

    return parsedPassports

def validHeight(heightString):
    v = {
        'cm': [150, 194],
        'in': [59,77]
    }
    p = re.compile('(\d+)(cm|in)')
    h = re.match(p, heightString)
    if h:
        if int(h.group(1)) in range(v[h.group(2)][0], v[h.group(2)][1]):
            return True

    return False

def part1():

    valid   = 0
    invalid = 0

    parsedPassports = parsePassports()
    validPassports  = []

    for passport in parsedPassports:
        # diff our passport keys from the def format
        missingKeys = set(passportStructure) - set(passport)

        # if no missing keys or if only missing cid mark as valid
        if len(missingKeys) == 0 or str(missingKeys) == "{'cid'}":
            valid += 1
            validPassports.append(passport)
        else:
            invalid +=1

    return validPassports

def part2():

    valid   = 0
    invalid = 0

    # grab passports from our first validation run
    part1Passports = part1()

    for passport in part1Passports:
        if (
            # check birth year >= 1920 and <= 2002
            int(passport['byr']) in range(1920,2003)
            # check issue year >= 2010 and <= 2020
            and int(passport['iyr']) in range(2010,2021)
            # check expiration year >= 2020 and <= 2030
            and int(passport['eyr']) in range(2020,2031)
            # check height cm >= 150 and <=193, or in >=59 and <= 76
            and validHeight(passport['hgt'])
            # check hair color valid hex code
            and re.match('^#[0-9a-f]{6}$', passport['hcl']) is not None
            # check eye color one of set values
            and passport['ecl'] in validEyeColors
            # passport number contains 9 digits
            and re.match('^\d{9}$', passport['pid']) is not None
        ):
            valid += 1
            print("valid: ", end='')
            print(passport)
        else:
            invalid += 1
            print("invalid: ", end='')
            print(passport)

    print(valid)

if __name__ == "__main__":
    print(len(part1()))
    part2()
