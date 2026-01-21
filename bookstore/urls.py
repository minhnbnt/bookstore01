"""
URL configuration for bookstore project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home_view(request):
    """Home page view."""
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('cart/', include('cart.urls')),
]
