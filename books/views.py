from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Book, SaleCampaign


def book_list(request):
    """Display list of all books with pagination."""
    books = Book.objects.all().order_by("-created_at")
    paginator = Paginator(books, 12)  # 12 books per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get active campaigns for display
    now = timezone.now()
    active_campaigns = SaleCampaign.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now,
    ).order_by("-discount_percentage")[:3]

    return render(
        request,
        "books/book_list.html",
        {
            "page_obj": page_obj,
            "books": page_obj.object_list,
            "active_campaigns": active_campaigns,
        },
    )


def book_detail(request, book_id):
    """Display details of a single book."""
    book = get_object_or_404(Book, id=book_id)

    # Get active campaign for this book
    active_campaign = book.get_active_campaign()

    # Get related books on sale (exclude current book)
    now = timezone.now()
    related_sale_books = (
        Book.objects.filter(
            sale_campaigns__is_active=True,
            sale_campaigns__start_date__lte=now,
            sale_campaigns__end_date__gte=now,
        )
        .exclude(id=book_id)
        .distinct()[:4]
    )

    return render(
        request,
        "books/book_detail.html",
        {
            "book": book,
            "active_campaign": active_campaign,
            "related_sale_books": related_sale_books,
        },
    )


def sale_campaigns(request):
    """Display all sale campaigns."""
    now = timezone.now()

    # Active campaigns
    ongoing_campaigns = (
        SaleCampaign.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
        .prefetch_related("books")
        .order_by("-discount_percentage")
    )

    # Upcoming campaigns
    upcoming_campaigns = (
        SaleCampaign.objects.filter(
            is_active=True,
            start_date__gt=now,
        )
        .prefetch_related("books")
        .order_by("start_date")
    )

    return render(
        request,
        "books/sale_campaigns.html",
        {
            "ongoing_campaigns": ongoing_campaigns,
            "upcoming_campaigns": upcoming_campaigns,
        },
    )


def sale_campaign_detail(request, campaign_id):
    """Display details of a sale campaign and its books."""
    campaign = get_object_or_404(SaleCampaign, id=campaign_id)
    books = campaign.books.all().order_by("title")

    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "books/sale_campaign_detail.html",
        {
            "campaign": campaign,
            "page_obj": page_obj,
            "books": page_obj.object_list,
        },
    )
