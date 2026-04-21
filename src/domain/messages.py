"""
统一错误和成功消息

集中管理所有用户-facing的消息，保持一致性
"""


class ErrorMessages:
    """错误消息"""

    # 玩家相关
    EMPTY_NAME = "Name cannot be empty."
    INVALID_NAME_LENGTH = "Name must be {min}-{max} characters long."
    NAME_EXISTS = "Name '{name}' already exists. Please choose another."
    PLAYER_NOT_FOUND = "Player not found."

    # 物品相关
    ITEM_NOT_FOUND = "Item not found in backpack."
    ITEM_NOT_FOUND_GENERIC = "Item not found."
    INSUFFICIENT_QUANTITY = "Invalid quantity. You have {quantity}."
    NOT_ENOUGH_ITEMS = "Not enough items. Have {quantity}."

    # 价格相关
    INVALID_PRICE_RANGE = "Price must be between {min:.0f} and {max:.0f}."
    INVALID_PRICE = "Invalid price."

    # 金币相关
    INSUFFICIENT_GOLD = "Insufficient gold. Need {need:.0f}, have {have:.0f}."
    INSUFFICIENT_GOLD_SHORT = "Insufficient gold."
    CANNOT_DEDUCT = "Cannot deduct gold."

    # 交易相关
    ORDER_NOT_FOUND = "Order not found."
    ORDER_NOT_AVAILABLE = "This order is no longer available."
    CANNOT_BUY_OWN = "You cannot buy your own listing."
    INVALID_QUANTITY = "Invalid quantity. Available: {available}."

    # 搜索相关
    EMPTY_KEYWORD = "Search keyword cannot be empty."

    # 通用
    INVALID_NUMBER = "Please enter a valid number."
    INVALID_CHOICE = "Invalid choice. Please try again."
    OPERATION_FAILED = "Operation failed."
    TRANSACTION_FAILED = "Transaction failed."


class SuccessMessages:
    """成功消息"""

    # 玩家相关
    PLAYER_CREATED = "Player created successfully. Welcome to the game!"
    GOLD_UPDATED = "Gold updated successfully."

    # 物品相关
    ITEM_ADDED = "Item added successfully."
    ITEM_SOLD = "Sold {quantity}x {item} for {gold:.0f} gold."
    ITEM_DEDUCTED = "Item deducted successfully."

    # 交易相关
    ITEM_LISTED = "Listed {quantity}x {item} at {price:.0f} gold each."
    ITEM_BOUGHT = "Successfully bought {quantity}x {item}."
    ITEM_DELISTED = "Item delisted successfully."

    # 存档相关
    GAME_SAVED = "Game saved successfully."
    GAME_LOADED = "Game loaded successfully."

    # 通用
    OPERATION_SUCCESS = "Operation successful."
    WELCOME_BACK = "Welcome back, {name}!"


class InfoMessages:
    """信息提示"""

    PRESS_ENTER_CONTINUE = "Press Enter to continue..."
    CONFIRM_ACTION = "Are you sure? (y/n): "
    NO_ITEMS_BACKPACK = "Your backpack is empty."
    NO_LISTINGS = "No active listings."
    NO_RECORDS = "No records found."
