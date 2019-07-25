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


def is_hanzi(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_other(uchar):
    """非中文 非数字 非英文字母 """
    return not (is_hanzi(uchar) or is_alphabet(uchar) or is_number(uchar))


def common_ljust(string, width, fillchar=" "):
    """支持中英文字符对齐"""
    string = str(string)
    string_width = sum(map(lambda x: 2 if len(x.encode("utf-8")) > 2 else 1, string))
    assert width >= string_width
    return string + fillchar * (width-string_width)


if __name__ == "__main__":
    # print(quanjiao2banjiao("京东方Ａ"))
    for c in "京东方Ａ":
        print(c, is_hanzi(c) or is_other(c))
