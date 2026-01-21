from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'get_item_count', 'get_total']
    search_fields = ['customer__name', 'customer__email']
    list_filter = ['created_at']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book', 'quantity', 'get_subtotal', 'added_at']
    search_fields = ['book__title', 'cart__customer__name']
    list_filter = ['added_at']
