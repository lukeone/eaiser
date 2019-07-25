# -*- coding: utf-8 -*-

import pytest

from easier.topic.stock import Stock
from easier.context import Context


@pytest.fixture(scope="module")
def topic():
    context = Context()

    topic = Stock(context)
    context.set_current(topic)

    yield topic

    topic.release()


@pytest.mark.usefixtures("topic")
class TestStock(object):

    def test_normalize(self, topic):

        assert topic.normalize("中国平安") == ["601318"]
        assert topic.normalize(["中国平安"]) == ["601318"]
        assert sorted(topic.normalize(["中国平安", "000725"])) == sorted(["601318", "000725"])

        indexs = topic.normalize(["上证指数", "深圳成指", "沪深300指数", "上证50", "中小板", "创业板"])
        indexs_std = ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']
        assert sorted(indexs) == sorted(indexs_std)

    def test_get_realtime_quotation(self, topic):
        assert topic.get_realtime_quotation([""]) is None
        assert len(topic.get_realtime_quotation(["中国平安"])) == 1
        assert len(topic.get_realtime_quotation(["中国平安", "000725"])) == 2

    def test_get_stock_basis(self, topic):
        basis = topic.get_stock_basis([""])
        assert basis is None or basis.empty

        assert len(topic.get_stock_basis(["中国平安"])) == 1
        assert len(topic.get_stock_basis(["中国平安", "000725"])) == 2
