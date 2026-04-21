"""
Repository 层单元测试

测试数据持久化操作（使用临时目录隔离）
"""

import pytest
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture
def temp_data_dir(tmp_path):
    """临时数据目录"""
    data_dir = tmp_path / "src" / "data"
    data_dir.mkdir(parents=True)
    return str(data_dir)


class TestRepositoryConstants:
    """测试仓库常量"""

    def test_item_config_loaded(self):
        """验证物品配置已加载"""
        from src.repository import ITEM_CONFIG
        assert isinstance(ITEM_CONFIG, dict)
        assert len(ITEM_CONFIG) > 0

    def test_initial_backpack_loaded(self):
        """验证初始背包配置已加载"""
        from src.repository import INITIAL_BACKPACK
        assert isinstance(INITIAL_BACKPACK, list)
        assert len(INITIAL_BACKPACK) > 0


class TestDataInitializer:
    """测试数据初始化"""

    def test_data_dir_configuration(self, temp_data_dir):
        """测试数据目录配置"""
        from src.repository import data_initializer as di
        original_dir = di.DATA_DIR
        di.DATA_DIR = temp_data_dir

        # 创建初始化文件
        di.initialize()

        # 验证文件存在
        assert os.path.exists(os.path.join(temp_data_dir, "players.json"))
        assert os.path.exists(os.path.join(temp_data_dir, "items.json"))
        assert os.path.exists(os.path.join(temp_data_dir, "listings.json"))

        di.DATA_DIR = original_dir
