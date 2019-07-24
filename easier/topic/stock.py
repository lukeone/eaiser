# -*- coding: utf-8 -*-
import curses
import time
import tushare
import tableprint

from .core import Topic, entrypoint
from ..util import pandas_to_list, CurseHelper, quanjiao2banjiao
from pypinyin import Style, pinyin


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
        
        :param stocks: string of stock code or list of stock codes
        :return: DataFrame object
        """
        assert stocks is not None
        codes = self.normalize(stocks)
        df = tushare.get_realtime_quotes(codes)
        if df is None:
            return

        df.reset_index()
        for field in ["open", "price", "low", "high", "pre_close"]:
            df[field] = df[field].astype('float64')
        df.round(2)

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

    def _calculate_price_changed(self, price, pre_close):
        """ compute percentage of stock price rise

        :param price: current stock price
        :param pre_close: last day close price
        :return: tuple, (ratio, color, symbol)
        """
        price, pre_close = float(price), float(pre_close)
        diff = price - pre_close
        ratio = diff / pre_close

        if diff > 0: return ratio, CurseHelper.RED, "+"
        elif diff < 0: return ratio, CurseHelper.GREEN, ""
        else: return ratio, CurseHelper.YELLOW, ""

    @entrypoint(doc="show stock realtime price")
    def watch(self, stocks=None):
        stocks = stocks.split(" ")

        curse = CurseHelper()
        curse.scr.clear()

        columns = ["code", "name", "open", "low", "high", "price"]
        width = 10
        tpl0 = "".join(["{%s:<%d}" % (c, width) for c in columns])
        tpl1 = "{:<%ds}" % width

        # header
        def _add_header():
            row0 = tpl0.format(**dict(zip(columns, columns)))
            row1 = tpl1.format("percentage")
            curse.scr.addstr(0, 0, row0, curses.color_pair(CurseHelper.CYAN))
            curse.scr.addstr(0, len(row0.encode("utf-8")), row1, curses.color_pair(CurseHelper.CYAN))

        def _add_row(i, d):
            row0 = tpl0.format(**d)
            row1 = tpl1.format(d["percentage"])
            curse.scr.addstr(i+1, 0, row0)
            curse.scr.addstr(i+1, len(row0.encode("utf-8")), row1, curses.color_pair(d["color"]))

        _add_header()
        try:
            while 1:
                quotation = self.get_realtime_quotation(stocks)
                records = pandas_to_list(quotation)

                for d in records:
                    name = quanjiao2banjiao(d["name"])
                    d["name"] = "".join([c[0].upper() for c in pinyin(name, style=Style.FIRST_LETTER)])
                    ratio, color, sig = self._calculate_price_changed(d["price"], d["pre_close"])
                    percentage = "%s%.2f%%" % (sig, ratio * 100)
                    d.update({"ratio": ratio, "color": color, "percentage": percentage})

                records.sort(key=lambda item: -item["ratio"])
                for idx, d in enumerate(records):
                    _add_row(idx, d)

                curse.scr.refresh()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            curse.finish()
