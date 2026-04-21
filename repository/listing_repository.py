import json
import os
from typing import Optional
from domain.market_listing import MarketListing

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "listings.json")


class ListingRepository:
    def __init__(self, path: str = DATA_PATH):
        self._path = os.path.abspath(path)
        self._listings: dict[str, MarketListing] = {}
        self.load()

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            self._listings = {d["listing_id"]: MarketListing.from_dict(d) for d in data}

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([l.to_dict() for l in self._listings.values()], f, ensure_ascii=False, indent=2)

    def find_by_id(self, listing_id: str) -> Optional[MarketListing]:
        return self._listings.get(listing_id)

    def find_active(self) -> list[MarketListing]:
        return [l for l in self._listings.values() if l.status == "active"]

    def find_by_seller(self, seller_id: str) -> list[MarketListing]:
        return [l for l in self._listings.values() if l.seller_id == seller_id]

    def find_by_item(self, item_id: str) -> list[MarketListing]:
        return [l for l in self._listings.values() if l.item_id == item_id and l.status == "active"]

    def all(self) -> list[MarketListing]:
        return list(self._listings.values())

    def save_listing(self, listing: MarketListing):
        self._listings[listing.listing_id] = listing
        self.save()

    def delete(self, listing_id: str) -> bool:
        if listing_id in self._listings:
            del self._listings[listing_id]
            self.save()
            return True
        return False
