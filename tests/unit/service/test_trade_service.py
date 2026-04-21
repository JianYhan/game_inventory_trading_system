"""
TradeService 单元测试

测试交易记录相关的业务逻辑
"""

import pytest
from src.service.trade_service import TradeService


class TestTradeServiceBasic:
    """基础测试"""

    def test_trade_service_creation(self):
        """创建服务"""
        service = TradeService()
        assert service is not None

    def test_record_queue_exists(self):
        """验证记录队列存在"""
        service = TradeService()
        assert service._record_queue is not None

    def test_buy_records_list_exists(self):
        """验证购买记录列表存在"""
        service = TradeService()
        assert service._buy_records is not None

    def test_sell_records_list_exists(self):
        """验证出售记录列表存在"""
        service = TradeService()
        assert service._sell_records is not None
