from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Book, Cart

class BookRepository(ABC):
    @abstractmethod
    def list_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def save(self, book: Book):
        pass

class CartRepository(ABC):
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def create_for_customer(self, customer_id: int) -> Cart:
        pass

    @abstractmethod
    def save(self, cart: Cart):
        pass
    
    @abstractmethod
    def add_item(self, cart_id: int, book_id: int, quantity: int):
        pass
        
    @abstractmethod
    def remove_item(self, cart_id: int, item_id: int):
        pass
    
    @abstractmethod
    def update_item_quantity(self, cart_id: int, item_id: int, quantity: int):
        pass
