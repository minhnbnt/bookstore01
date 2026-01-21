from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from infrastructure.django_repositories import DjangoCartRepository, DjangoBookRepository
from usecases.cart_usecases import (
    AddToCartUseCase, 
    ViewCartUseCase, 
    RemoveFromCartUseCase, 
    UpdateQuantityUseCase
)

# Dependency Injection
cart_repo = DjangoCartRepository()
book_repo = DjangoBookRepository()

add_to_cart_use_case = AddToCartUseCase(cart_repo, book_repo)
view_cart_use_case = ViewCartUseCase(cart_repo)
remove_from_cart_use_case = RemoveFromCartUseCase(cart_repo)
update_quantity_use_case = UpdateQuantityUseCase(cart_repo)


def get_or_create_cart(request):
    """Helper - logic moved to UseCases mostly, but kept if needed by simple views or internal"""
    # Not used directly anymore ideally
    pass


def cart_view(request):
    """Display shopping cart contents."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Please login to view your cart.')
        return redirect('login')
    
    cart = view_cart_use_case.execute(customer_id)
    # The template expects 'cart' and 'items'. 
    # My Cart entity has 'items'.
    # items = cart.items.select_related('book').all() if cart else [] # OLD
    items = cart.items if cart else []
    
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
    
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        add_to_cart_use_case.execute(customer_id, book_id, quantity)
        
        # Need book title for message. 
        # Ideally use case returns it or we fetch it. 
        # Pruning fetch for performance vs Clean simplicity.
        # Let's fetch just for message or generic message.
        # Or better, AddToCartUseCase could return the book or result.
        # keeping it simple:
        messages.success(request, 'Added to your cart!')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('book_detail', book_id=book_id)
    except Exception as e:
         messages.error(request, "An error occurred.")
         print(e)
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    if request.method != 'POST':
        return redirect('cart')
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    
    try:
        remove_from_cart_use_case.execute(customer_id, item_id)
        messages.success(request, 'Item removed from cart.')
    except Exception:
        messages.error(request, 'Error removing item.')
    
    return redirect('cart')


def update_quantity(request, item_id):
    """Update quantity of a cart item."""
    if request.method != 'POST':
        return redirect('cart')
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        # Handling delete logic in view or use case?
        # My UseCase handles update. 0 usually means delete in some logic, 
        # but here logic: if < 1 delete.
        if quantity < 1:
             remove_from_cart_use_case.execute(customer_id, item_id)
             messages.success(request, 'Item removed from cart.')
        else:
             update_quantity_use_case.execute(customer_id, item_id, quantity)
             messages.success(request, 'Cart updated.')
    except ValueError as e:
        messages.error(request, str(e))
    except Exception:
        messages.error(request, 'Error updating cart.')
    
    return redirect('cart')
