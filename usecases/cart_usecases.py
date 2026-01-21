from typing import Optional
from domain.entities import Cart, Book
from domain.repositories import CartRepository, BookRepository

class AddToCartUseCase:
    def __init__(self, cart_repo: CartRepository, book_repo: BookRepository):
        self.cart_repo = cart_repo
        self.book_repo = book_repo

    def execute(self, customer_id: int, book_id: int, quantity: int):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        
        if book.stock < quantity:
            raise ValueError(f"Insufficient stock. Only {book.stock} available.")
            
        cart = self.cart_repo.get_by_customer_id(customer_id)
        if not cart:
            cart = self.cart_repo.create_for_customer(customer_id)
        
        self.cart_repo.add_item(cart.id, book_id, quantity)

class ViewCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    def execute(self, customer_id: int) -> Optional[Cart]:
        return self.cart_repo.get_by_customer_id(customer_id)

class RemoveFromCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    def execute(self, customer_id: int, item_id: int):
        cart = self.cart_repo.get_by_customer_id(customer_id)
        if cart:
            self.cart_repo.remove_item(cart.id, item_id)

class UpdateQuantityUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo
    
    def execute(self, customer_id: int, item_id: int, quantity: int):
        cart = self.cart_repo.get_by_customer_id(customer_id)
        if cart:
             # Ideally we check stock here too, but for simplicity assuming repo or UI handles basic checks
             # Actually, checking stock is business logic.
             # We need book info. But we only have item_id. 
             # To do it properly:
             # 1. Get cart
             # 2. Find item in cart (entity)
             # 3. Check stock on item.book
             # 4. If ok, repo.update
             
             # Finding item in cart:
             item = next((i for i in cart.items if i.id == item_id), None)
             if item:
                 if quantity > item.book.stock:
                     raise ValueError(f"Only {item.book.stock} copies available.")
                 self.cart_repo.update_item_quantity(cart.id, item_id, quantity)
