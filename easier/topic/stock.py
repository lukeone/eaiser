# -*- coding: utf-8 -*-
import curses
import time
import tushare

from .core import Topic, entrypoint
from ..util import pandas_to_list, CurseHelper, common_ljust


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

            > normalize(["上证指数", "深圳成指"])

        :param stocks:
        :return: string of stock code, or list
        """
        # indexs = topic.normalize(["上证指数", "深圳成指", "沪深300指数", "上证50", "中小板", "创业板"])
        # indexs_std = ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']
        index_data = {
            "上证指数": "sh",
            "深圳成指": "sz",
            "沪深300指数": "hs300",
            "上证50": "sz50",
            "中小板": "zxb",
            "创业板": "cyb"
        }

        self.check_load_stock_basis()
        if isinstance(stocks, str):
            stocks = [stocks]
        else:
            stocks = list(stocks)

        indexes = []
        for code in stocks:
            if code in index_data:
                indexes.append(index_data[code])
                continue
            if code in index_data.values():
                indexes.append(code)

        basis = self._stock_basis
        stocks = basis[basis["name"].isin(stocks) | basis["code"].isin(stocks)]["code"].to_list()
        return indexes + stocks

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

        if diff > 0:
            return ratio, CurseHelper.RED, "+"
        elif diff < 0:
            return ratio, CurseHelper.GREEN, ""
        else:
            return ratio, CurseHelper.YELLOW, ""

    @entrypoint(doc="show stock realtime price")
    def watch(self, stocks=None):
        stocks = stocks.split(" ")

        curse = CurseHelper()
        curse.scr.clear()

        width = 12
        columns = ["code", "name", "open", "low", "high", "price"]

        # header
        def _add_header():
            row0 = "".join([common_ljust(s, width) for s in columns])
            row1 = common_ljust("percentage", width)
            curse.scr.addstr(0, 0, row0, curses.color_pair(CurseHelper.CYAN))
            curse.scr.addstr(0, len(columns) * width, row1, curses.color_pair(CurseHelper.CYAN))

        def _add_row(i, d):
            row0 = "".join(common_ljust(d[col], width) for col in columns)
            row1 = common_ljust(d["percentage"], width)
            curse.scr.addstr(i+1, 0, row0)
            curse.scr.addstr(i+1, len(columns) * width, row1, curses.color_pair(d["color"]))

        _add_header()
        try:
            while 1:
                quotation = self.get_realtime_quotation(stocks)
                records = pandas_to_list(quotation)

                for d in records:
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
