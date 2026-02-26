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

    def get_active_campaign(self):
        """Get the best active sale campaign for this book."""
        if not self.pk:
            return None
        now = timezone.now()
        active_campaigns = self.sale_campaigns.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        ).order_by("-discount_percentage")
        return active_campaigns.first()

    def get_sale_price(self):
        """Get the discounted price if there's an active campaign."""
        campaign = self.get_active_campaign()
        if campaign:
            return campaign.get_discounted_price(self.price)
        return None

    def get_final_price(self):
        """Get the final price (sale price or original price)."""
        sale_price = self.get_sale_price()
        return sale_price if sale_price else self.price

    def get_discount_percentage(self):
        """Get the discount percentage if there's an active campaign."""
        campaign = self.get_active_campaign()
        if campaign:
            return campaign.discount_percentage
        return None

    def is_on_sale(self):
        """Check if book is currently on sale."""
        return self.get_active_campaign() is not None


class SaleCampaign(models.Model):
    """Sale Campaign entity: quản lý chiến dịch giảm giá cho sách."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, related_name="sale_campaigns", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sale_campaigns"
        verbose_name = "Sale Campaign"
        verbose_name_plural = "Sale Campaigns"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}%)"

    def is_ongoing(self):
        """Check if campaign is currently active."""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def get_discounted_price(self, original_price):
        """Calculate discounted price based on campaign discount percentage."""
        discount_amount = original_price * (self.discount_percentage / Decimal("100"))
        return (original_price - discount_amount).quantize(Decimal("0.01"))

    def get_status(self):
        """Get the current status of the campaign."""
        now = timezone.now()
        if not self.is_active:
            return "inactive"
        if now < self.start_date:
            return "upcoming"
        if now > self.end_date:
            return "expired"
        return "ongoing"

    def get_status_display_class(self):
        """Get CSS class for status badge."""
        status_classes = {
            "ongoing": "bg-green-100 text-green-700",
            "upcoming": "bg-blue-100 text-blue-700",
            "expired": "bg-gray-100 text-gray-700",
            "inactive": "bg-red-100 text-red-700",
        }
        return status_classes.get(self.get_status(), "bg-gray-100 text-gray-700")
