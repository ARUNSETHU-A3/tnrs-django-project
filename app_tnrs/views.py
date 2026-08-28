from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Products, Order
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from functools import wraps
from django.views.decorators.http import require_POST


class CartItem:
    """Helper class to ensure cart items work reliably in templates"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@login_required(login_url='login')
def home(request):
    products = Products.objects.all()
    products = Products.objects.filter(is_available=True)
    return render(request, 'home.html', {'products': products})

@login_required(login_url='login')
def cart(request):
    cart_raw = request.session.get('cart', [])
    cart_items = [CartItem(**item) for item in cart_raw]
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])
    product = get_object_or_404(Products, id=item_id)
    item=({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float (product.price),
    })
    cart.append(item)
    request.session['cart'] = cart
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    if 0 <= item_id < len(cart):
        cart.pop(item_id)
    else:
        # If item_id is out of range, remove the item by its id instead
        cart = [item for item in cart if item['id'] != item_id]
    request.session['cart'] = cart
    return redirect('cart')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
 
def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)
@login_required
def buy_product(request, item_id):
    product = get_object_or_404(Products, id=item_id)

    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            mobile = request.POST.get('mobile', '').strip()
            address = request.POST.get('address', '').strip()

            if not name or not mobile or not address:
                return render(request, "order.html", {
                    "product": product,
                    "error": "All fields are required"
                })

            # Create order
            order = Order.objects.create(
                user=request.user,
                product=product,
                name=name,
                mobile=mobile,
                address=address
            )

            # Remove from cart
            cart = request.session.get('cart', [])
            cart = [item for item in cart if item['id'] != item_id]
            request.session['cart'] = cart
            request.session.modified = True

            # Mark product as unavailable
            product.is_available = False
            product.save()

            return redirect('order_confirmation', order_id=order.id)
        except Exception as e:
            return render(request, "order.html", {
                "product": product,
                "error": f"An error occurred: {str(e)}"
            })

    return render(request, "order.html", {"product": product})


@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, "view_orders.html", {"orders": orders})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_confirmation.html", {"order": order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    product = order.product
    
   
    product.is_available = True
    product.save()
    

    order.delete()
    
    return redirect('home')


def _superuser_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped


@_superuser_required
def admin_dashboard(request):
    products = Products.objects.all().order_by('name')
    orders = Order.objects.select_related('user', 'product').all().order_by('-ordered_at')
    return render(request, 'admin_dashboard/dashboard.html', {'products': products, 'orders': orders})


@_superuser_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProductForm()
    return render(request, 'admin_dashboard/product_form.html', {'form': form, 'create': True})


@_superuser_required
def product_edit(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_dashboard/product_form.html', {'form': form, 'create': False, 'product': product})


@_superuser_required
def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted')
        return redirect('admin_dashboard')
    return render(request, 'admin_dashboard/product_confirm_delete.html', {'product': product})


@_superuser_required
@require_POST
def product_toggle_availability(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.is_available = not product.is_available
    product.save()
    return redirect('admin_dashboard')


@_superuser_required
@require_POST
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
    return redirect('admin_dashboard')