# -*- coding: utf-8 -*-
import re

pattern = re.compile(r"(?P<cmd>\w+) ?(?P<content>.*)?")


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
    lst = [ {} for i in range(len(dataframe))]
    for column, dict_val in dataframe.to_dict().items():
        for idx, val in dict_val.items():
            lst[idx][column] = val
    return lst


if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame([[1, 1], [2, 2]], columns=["A", "B"])
    print(pandas_to_list(df))
