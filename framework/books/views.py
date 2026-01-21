from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from infrastructure.django_repositories import DjangoBookRepository
from usecases.book_usecases import ListBooksUseCase, GetBookDetailUseCase

# Initialize repositories and use cases (Simple dependency injection)
book_repo = DjangoBookRepository()
list_books_use_case = ListBooksUseCase(book_repo)
get_book_detail_use_case = GetBookDetailUseCase(book_repo)

def book_list(request):
    """Display list of all books with pagination."""
    # books = Book.objects.all().order_by('-created_at') # Old
    books = list_books_use_case.execute()
    
    # Paginator expects list or QuerySet. List of entities works fine.
    paginator = Paginator(books, 12)  # 12 books per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'books': page_obj.object_list,
    })


def book_detail(request, book_id):
    """Display details of a single book."""
    # book = get_object_or_404(Book, id=book_id) # Old
    book = get_book_detail_use_case.execute(book_id)
    
    if not book:
        # Fallback to 404 if not found
        from django.http import Http404
        raise Http404("Book not found")

    return render(request, 'books/book_detail.html', {'book': book})
