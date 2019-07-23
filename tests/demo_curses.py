# -*- coding: utf-8 -*-

import curses
import time


def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        idx = 0
        while 1:
            idx += 1
            for i in range(3):
                stdscr.addstr(i, 0, "row:%s" % idx)
            stdscr.refresh()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":
    main()
