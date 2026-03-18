from __future__ import annotations
from datetime import datetime


class MarketListing:
    def __init__(self, listing_id: str, seller_id: str, item_id: str,
                 quantity: int, price_per_unit: float,
                 created_at: str = None, status: str = "active"):
        self.listing_id = listing_id
        self.seller_id = seller_id
        self.item_id = item_id
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.created_at = created_at or datetime.now().isoformat()
        self.status = status  # active | sold | cancelled

    def total_price(self) -> float:
        return self.quantity * self.price_per_unit

    def to_dict(self) -> dict:
        return {
            "listing_id": self.listing_id,
            "seller_id": self.seller_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "created_at": self.created_at,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MarketListing":
        return cls(
            data["listing_id"], data["seller_id"], data["item_id"],
            data["quantity"], data["price_per_unit"],
            data.get("created_at"), data.get("status", "active")
        )

    def __repr__(self):
        return f"Listing({self.listing_id}: {self.item_id} x{self.quantity} @{self.price_per_unit})"
