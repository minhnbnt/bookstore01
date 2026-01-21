from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book


def book_list(request):
    """Display list of all books with pagination."""
    books = Book.objects.all().order_by('-created_at')
    paginator = Paginator(books, 12)  # 12 books per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'books': page_obj.object_list,
    })


def book_detail(request, book_id):
    """Display details of a single book."""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})
