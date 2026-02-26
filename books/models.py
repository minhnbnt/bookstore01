from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Book(models.Model):
    """Book entity: id, title, author, price, stock."""

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"

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


class SaleCampaign(models.Model):
    """Sale Campaign entity: quản lý chiến dịch giảm giá cho sách."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, related_name="sale_campaigns")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sale_campaigns"
        verbose_name = "Sale Campaign"
        verbose_name_plural = "Sale Campaigns"

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}%)"

    def is_ongoing(self):
        """Check if campaign is currently active."""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def get_discounted_price(self, original_price):
        """Calculate discounted price based on campaign discount percentage."""
        discount_amount = original_price * (self.discount_percentage / Decimal("100"))
        return original_price - discount_amount
