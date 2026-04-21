"""
PlayerService 单元测试

测试玩家相关的业务逻辑
"""

import pytest
from src.service.player_service import PlayerService


class TestPlayerServiceBasic:
    """基础测试"""

    def test_player_service_creation(self):
        """创建服务"""
        service = PlayerService()
        assert service is not None

    def test_player_tables_exist(self):
        """验证玩家表存在"""
        service = PlayerService()
        assert service._player_table is not None
        assert service._name_table is not None


class TestPlayerServiceConstants:
    """常量测试"""

    def test_initial_gold(self):
        """验证初始金币配置"""
        from src.domain import PlayerConfig
        assert PlayerConfig.INITIAL_GOLD == 1000.0

    def test_name_length_limits(self):
        """验证名称长度限制"""
        from src.domain import PlayerConfig
        assert PlayerConfig.MIN_NAME_LENGTH == 2
        assert PlayerConfig.MAX_NAME_LENGTH == 12
