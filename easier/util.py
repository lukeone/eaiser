# -*- coding: utf-8 -*-
import re
import curses

pattern = re.compile(r"(?P<cmd>\w+) ?(?P<content>.*)?")


class CurseHelper(object):

    RED = 1
    GREEN = 2
    YELLOW = 3
    CYAN = 4

    def __init__(self):
        self.scr = None
        self.init()

    def init(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self.YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.scr = stdscr

    def finish(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()


def parse_command(text):
    """extract command and command content from input text

        such as:
            parse_command("select_topic plan")
            >> {"command": "select_topic", "content": "plan"}

    :param text: the input text
    :return:
    """
    match = pattern.match(text)
    if match:
        return match.groupdict()
    return None


def pandas_to_list(dataframe):
    """
    trans dataframe to dict, what different from `DataFrame.to_dict` is that use
    column name as dict key.

            import pandas as pd
            df = pd.DataFrame([[1, 1], [2, 2]], columns=["A", "B"])
            print(pandas_to_list(df))   # output: [{'A': 1, 'B': 1}, {'A': 2, 'B': 2}]


    :param dataframe:
    :return: list object
    """
    lst = [{} for i in range(len(dataframe))]
    for column, dict_val in dataframe.to_dict().items():
        for idx, val in dict_val.items():
            lst[idx][column] = val
    return lst


def quanjiao2banjiao(ustring):
    """全角字符转半角
    """
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return "".join(ss)


if __name__ == "__main__":
    print(quanjiao2banjiao("京东方Ａ"))
