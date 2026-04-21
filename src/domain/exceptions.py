"""
统一异常处理和装饰器

提供 Service 层的异常捕获和日志记录
"""

import logging
import functools
from typing import Callable, Any
from .models import Response
from .messages import ErrorMessages

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class GameException(Exception):
    """游戏业务异常基类"""
    pass


class ValidationException(GameException):
    """验证异常"""
    pass


class InsufficientGoldException(GameException):
    """金币不足异常"""
    pass


class ItemNotFoundException(GameException):
    """物品不存在异常"""
    pass


class PlayerNotFoundException(GameException):
    """玩家不存在异常"""
    pass


def handle_exceptions(func: Callable) -> Callable:
    """
    统一异常处理装饰器

    用于 Service 层方法，捕获所有异常并返回 Response.fail
    同时记录日志
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ValidationException as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            return Response.fail(str(e))
        except InsufficientGoldException as e:
            logger.warning(f"Gold insufficient in {func.__name__}: {str(e)}")
            return Response.fail(str(e))
        except ItemNotFoundException as e:
            logger.warning(f"Item not found in {func.__name__}: {str(e)}")
            return Response.fail(str(e))
        except PlayerNotFoundException as e:
            logger.warning(f"Player not found in {func.__name__}: {str(e)}")
            return Response.fail(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            return Response.fail(ErrorMessages.OPERATION_FAILED)
    return wrapper


def validate_non_empty(value: str, field_name: str = "Value") -> str:
    """验证非空"""
    if not value or not value.strip():
        raise ValidationException(f"{field_name} cannot be empty.")
    return value.strip()


def validate_range(value: int, min_val: int, max_val: int, field_name: str = "Value") -> int:
    """验证数值范围"""
    if not (min_val <= value <= max_val):
        raise ValidationException(f"{field_name} must be between {min_val} and {max_val}.")
    return value
