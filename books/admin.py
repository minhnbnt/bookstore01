from django.contrib import admin

from .models import Book, SaleCampaign


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "price",
        "get_final_price_display",
        "stock",
        "is_on_sale",
        "created_at",
    ]
    search_fields = ["title", "author"]
    list_filter = ["author", "created_at"]
    list_editable = ["price", "stock"]
    readonly_fields = ["created_at", "updated_at"]

    @admin.display(description="Sale Price")
    def get_final_price_display(self, obj):
        if obj.is_on_sale():
            return f"${obj.get_final_price()} (-{obj.get_discount_percentage()}%)"
        return "-"

    @admin.display(description="On Sale", boolean=True)
    def is_on_sale(self, obj):
        return obj.is_on_sale()


@admin.register(SaleCampaign)
class SaleCampaignAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "discount_percentage",
        "start_date",
        "end_date",
        "is_active",
        "get_status",
        "book_count",
        "created_at",
    ]
    search_fields = ["name", "description"]
    list_filter = ["is_active", "start_date", "end_date"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["books"]
    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Discount", {"fields": ("discount_percentage",)}),
        ("Schedule", {"fields": ("start_date", "end_date", "is_active")}),
        ("Books", {"fields": ("books",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.display(description="Status")
    def get_status(self, obj):
        return obj.get_status().capitalize()

    @admin.display(description="Books")
    def book_count(self, obj):
        return obj.books.count()
