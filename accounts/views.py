from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Customer


def register_view(request):
    """Handle customer registration."""
    if request.session.get('customer_id'):
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            customer = Customer(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
            )
            customer.set_password(form.cleaned_data['password'])
            customer.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle customer login."""
    if request.session.get('customer_id'):
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                customer = Customer.objects.get(email=email)
                if customer.check_password(password):
                    request.session['customer_id'] = customer.id
                    request.session['customer_name'] = customer.name
                    messages.success(request, f'Welcome back, {customer.name}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle customer logout."""
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def profile_view(request):
    """Display customer profile."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Please login to view your profile.')
        return redirect('login')
    
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    return render(request, 'accounts/profile.html', {'customer': customer})
