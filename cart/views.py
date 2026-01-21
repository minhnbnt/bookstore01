from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book
from accounts.models import Customer


def get_or_create_cart(request):
    """Get existing cart or create a new one for the customer."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    cart, created = Cart.objects.get_or_create(customer=customer)
    return cart


def cart_view(request):
    """Display shopping cart contents."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Please login to view your cart.')
        return redirect('login')
    
    cart = get_or_create_cart(request)
    items = cart.items.select_related('book').all() if cart else []
    
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
    })


def add_to_cart(request, book_id):
    """Add a book to the cart."""
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Please login to add items to your cart.')
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > book.stock:
        messages.error(request, f'Sorry, only {book.stock} copies available.')
        return redirect('book_detail', book_id=book_id)
    
    cart = get_or_create_cart(request)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update quantity if item exists
        new_quantity = cart_item.quantity + quantity
        if new_quantity > book.stock:
            messages.error(request, f'Cannot add more. Only {book.stock} copies available.')
            return redirect('book_detail', book_id=book_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Updated "{book.title}" quantity in cart.')
    else:
        messages.success(request, f'Added "{book.title}" to your cart!')
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    if request.method != 'POST':
        return redirect('cart')
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    
    cart = get_or_create_cart(request)
    if not cart:
        return redirect('login')
    
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        book_title = item.book.title
        item.delete()
        messages.success(request, f'Removed "{book_title}" from your cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    
    return redirect('cart')


def update_quantity(request, item_id):
    """Update quantity of a cart item."""
    if request.method != 'POST':
        return redirect('cart')
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    
    cart = get_or_create_cart(request)
    if not cart:
        return redirect('login')
    
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            item.delete()
            messages.success(request, f'Removed "{item.book.title}" from your cart.')
        elif quantity > item.book.stock:
            messages.error(request, f'Only {item.book.stock} copies available.')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Cart updated.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    
    return redirect('cart')
