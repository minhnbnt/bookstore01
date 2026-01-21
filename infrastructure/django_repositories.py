from typing import List, Optional
from domain.entities import Book, Cart, CartItem
from domain.repositories import BookRepository, CartRepository

# Imports updated to assume 'framework' is in sys.path
from books.models import Book as DjangoBook
from cart.models import Cart as DjangoCart, CartItem as DjangoCartItem
from accounts.models import Customer as DjangoCustomer

class DjangoBookRepository(BookRepository):
    def list_books(self) -> List[Book]:
        try:
            django_books = DjangoBook.objects.all().order_by('-created_at')
            return [self._to_entity(db_book) for db_book in django_books]
        except Exception as e:
            print(f"Error listing books: {e}")
            return []

    def get_by_id(self, book_id: int) -> Optional[Book]:
        try:
            db_book = DjangoBook.objects.get(id=book_id)
            return self._to_entity(db_book)
        except DjangoBook.DoesNotExist:
            return None
    
    def save(self, book: Book):
        pass

    def _to_entity(self, db_book: DjangoBook) -> Book:
        return Book(
            id=db_book.id,
            title=db_book.title,
            author=db_book.author,
            price=db_book.price,
            stock=db_book.stock
        )

class DjangoCartRepository(CartRepository):
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        try:
             db_cart = DjangoCart.objects.filter(customer_id=customer_id).first()
             if db_cart:
                 return self._to_entity(db_cart)
             return None
        except Exception as e:
            return None

    def create_for_customer(self, customer_id: int) -> Cart:
        # Assumes customer exists.
        customer = DjangoCustomer.objects.get(id=customer_id)
        db_cart, created = DjangoCart.objects.get_or_create(customer=customer)
        return self._to_entity(db_cart)

    def save(self, cart: Cart):
        pass
    
    def add_item(self, cart_id: int, book_id: int, quantity: int):
        db_cart = DjangoCart.objects.get(id=cart_id)
        book = DjangoBook.objects.get(id=book_id)
        item, created = DjangoCartItem.objects.get_or_create(cart=db_cart, book=book)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

    def remove_item(self, cart_id: int, item_id: int):
        DjangoCartItem.objects.filter(id=item_id, cart_id=cart_id).delete()
    
    def update_item_quantity(self, cart_id: int, item_id: int, quantity: int):
        try:
            item = DjangoCartItem.objects.get(id=item_id, cart_id=cart_id)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
        except DjangoCartItem.DoesNotExist:
            pass

    def _to_entity(self, db_cart: DjangoCart) -> Cart:
        items = [
            CartItem(
                id=item.id,
                book=Book(
                    id=item.book.id, 
                    title=item.book.title, 
                    author=item.book.author, 
                    price=item.book.price, 
                    stock=item.book.stock
                ),
                quantity=item.quantity
            )
            for item in db_cart.items.all()
        ]
        return Cart(
            id=db_cart.id,
            customer_id=db_cart.customer.id, 
            items=items
        )
