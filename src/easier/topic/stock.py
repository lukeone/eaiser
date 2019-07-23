# -*- coding: utf-8 -*-
import curses
import time
import tushare
import tableprint

from .core import Topic, entrypoint
from ..util import pandas_to_list


class Stock(Topic):

    _name = "stock"
    _description = "stock market quotation"

    def __init__(self, *args, **kwargs):
        self._stock_basis = None
        super(Stock, self).__init__(*args, **kwargs)

    def get_realtime_quotation(self, stocks):
        """realtime realtime exchange data

            get_realtime_quotation("000725")
            get_realtime_quotation(["000001", "000725"])

            code：代码
            name:名称
            changepercent:涨跌幅
            trade:现价
            open:开盘价
            high:最高价
            low:最低价
            settlement:昨日收盘价
            volume:成交量
            turnoverratio:换手率
            amount:成交金额
            per:市盈率
            pb:市净率
            mktcap:总市值
            nmc:流通市值

        
        :param stocks: string of stock code or list of stock codes
        :return: DataFrame object
        """
        assert stocks is not None
        codes = self.normalize(stocks)
        df = tushare.get_realtime_quotes(codes)
        df.reset_index()
        return df

    def get_stock_basis(self, stocks=None):
        """
        stock basis infomation

        :param stocks: name or code or name list or code list
        :return: DataFrame object
        """
        self.check_load_stock_basis()
        codes = self.normalize(stocks)
        basis = self._stock_basis
        return basis[basis["code"].isin(codes)]

    def normalize(self, stocks):
        """
            > normalize(["中国平安", "000725"])
              ['000725', '601318']

            > normalize("中国平安")
              ['601318']

        :param stocks:
        :return: string of stock code, or list
        """
        self.check_load_stock_basis()
        if isinstance(stocks, str):
            stocks = [stocks]
        else:
            stocks = list(stocks)

        basis = self._stock_basis
        return basis[basis["name"].isin(stocks) | basis["code"].isin(stocks)]["code"].to_list()

    def check_load_stock_basis(self):
        if self._stock_basis is not None and self._stock_basis.size:
            return
        self._load_all_stock_basis()

    def _load_all_stock_basis(self):
        """
        load stock data to memory
        """
        basis = tushare.get_stock_basics()
        self._stock_basis = basis.reset_index()

    @entrypoint(doc="show stock realtime price")
    def watch(self, stocks=None):

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        try:
            while 1:
                quotation = self.get_realtime_quotation(stocks)
                records = pandas_to_list(quotation)
                for idx, d in enumerate(records):
                    stdscr.addstr(idx, 0, "{code:<10s}{name:<10s}{price}".format(**d))
                stdscr.refresh()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
