from __future__ import annotations
from datetime import datetime


class Trade:
    def __init__(self, trade_id: str, listing_id: str, buyer_id: str, seller_id: str,
                 item_id: str, quantity: int, price_per_unit: float,
                 total_price: float, traded_at: str = None):
        self.trade_id = trade_id
        self.listing_id = listing_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.item_id = item_id
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.total_price = total_price
        self.traded_at = traded_at or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "trade_id": self.trade_id,
            "listing_id": self.listing_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "total_price": self.total_price,
            "traded_at": self.traded_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Trade":
        return cls(
            data["trade_id"], data["listing_id"], data["buyer_id"], data["seller_id"],
            data["item_id"], data["quantity"], data["price_per_unit"],
            data["total_price"], data.get("traded_at")
        )

    def __repr__(self):
        return f"Trade({self.trade_id}: {self.buyer_id} bought {self.item_id} x{self.quantity})"
