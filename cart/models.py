from django.db import models

from accounts.models import Customer
from books.models import Book


class Cart(models.Model):
    """Cart entity: id, customer_id, created_at."""

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart #{self.id} - {self.customer.name}"

    def get_total(self):
        """Calculate total price of all items in cart (using sale prices)."""
        total = sum(item.get_subtotal() for item in self.items.all())
        return total

    def get_original_total(self):
        """Calculate total price without any discounts."""
        total = sum(item.get_original_subtotal() for item in self.items.all())
        return total

    def get_total_savings(self):
        """Calculate total savings from sale prices."""
        return self.get_original_total() - self.get_total()

    def get_item_count(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """CartItem entity: id, cart_id, book_id, quantity."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ["cart", "book"]

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

    def get_unit_price(self):
        """Get the unit price (sale price if on sale, otherwise original price)."""
        return self.book.get_final_price()

    def get_original_unit_price(self):
        """Get the original unit price without discount."""
        return self.book.price

    def get_subtotal(self):
        """Calculate subtotal for this cart item (using sale price)."""
        return self.get_unit_price() * self.quantity

    def get_original_subtotal(self):
        """Calculate subtotal without any discounts."""
        return self.book.price * self.quantity

    def get_savings(self):
        """Calculate savings for this cart item."""
        return self.get_original_subtotal() - self.get_subtotal()

    def is_on_sale(self):
        """Check if the book in this cart item is on sale."""
        return self.book.is_on_sale()

    def get_discount_percentage(self):
        """Get the discount percentage if the book is on sale."""
        return self.book.get_discount_percentage()
