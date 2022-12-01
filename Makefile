DAY=$(shell date +%-d)
YEAR=$(shell date +%Y)
FOLDER=$(shell date +%Y/day-%d)

today:
	mkdir -p $(FOLDER)
	touch $(FOLDER)/sample.txt
	touch $(FOLDER)/solution.py
	curl -s https://adventofcode.com/$(YEAR)/day/$(DAY)/input --cookie "session=${ADVENT_OF_CODE_COOKIE}" -o $(FOLDER)/data.txt
