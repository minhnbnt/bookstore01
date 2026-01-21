from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Book(models.Model):
    """Book entity: id, title, author, price, stock."""
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_in_stock(self):
        """Check if book is available in stock."""
        return self.stock > 0

    def reduce_stock(self, quantity):
        """Reduce stock by given quantity."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False
