from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock', 'created_at']
    search_fields = ['title', 'author']
    list_filter = ['author', 'created_at']
    list_editable = ['price', 'stock']
    readonly_fields = ['created_at', 'updated_at']
