#!/usr/bin/env python3
# print out all curses color numbers

import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    try:
        for i in range(0, 256):
            stdscr.addstr(str(i) + " ", curses.color_pair(i + 1))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()


curses.wrapper(main)
