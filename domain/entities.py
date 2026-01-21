from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

@dataclass
class Book:
    id: Optional[int]
    title: str
    author: str
    price: Decimal
    stock: int

    def reduce_stock(self, quantity: int) -> bool:
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

@dataclass
class CartItem:
    book: Book
    quantity: int
    id: Optional[int] = None # Added ID

    @property
    def subtotal(self) -> Decimal:
        return self.book.price * self.quantity

    def get_subtotal(self) -> Decimal:
        # Template calls methods or properties. get_subtotal is called as property if no args in django template?
        # In django templates: {{ item.get_subtotal }} calls the method if it doesn't take arguments.
        return self.subtotal

@dataclass
class Cart:
    id: Optional[int]
    customer_id: int
    items: List[CartItem]

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    def get_total(self) -> Decimal:
        return self.total
    
    def get_item_count(self) -> int:
        return self.item_count
