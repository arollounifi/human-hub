from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, Order, ShippingAddress, PaymentInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ShippingAddressForm, PaymentInfoForm


def home(request):
    products = Product.objects.all()[:6]  # get the first 6 products
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


def category_list(request):  # This view will list all the product categories.
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()  # create a blank form
    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    customer_orders = Order.objects.filter(user=request.user)
    return render(request, 'store/profile.html', {'customer': request.user, 'customer_orders': customer_orders})



@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = sum([item.get_total() for item in cart.cartitem_set.all()])
    return render(request, 'store/cart.html', {'cart': cart, 'total': total})


@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, id=product_id)

    # Use get_or_create to avoid error if Cart does not exist yet
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': quantity})
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return redirect('home')


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST['cart_item_id']
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user == request.user:
            cart_item.delete()
        return redirect('view_cart')


@login_required
def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST['cart_item_id']
        quantity = int(request.POST['quantity'])
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user == request.user:
            cart_item.quantity = quantity
            cart_item.save()
        return redirect('view_cart')


from django.contrib import messages

@login_required
def checkout(request):
    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST, prefix='shipping')
        payment_form = PaymentInfoForm(request.POST, prefix='payment')

        if shipping_form.is_valid() and payment_form.is_valid():
            # Get the user's cart
            cart = Cart.objects.get(user=request.user)

            # Calculate the total
            total = sum([item.get_total() for item in cart.cartitem_set.all()])

            # Create the shipping address
            shipping_address = shipping_form.save()

            # Create the payment information
            payment_info = payment_form.save()

            # Create the order
            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address=shipping_address,
                payment_info=payment_info
            )

            # Associate the CartItems with the Order
            for item in cart.cartitem_set.all():
                order.cart_items.add(item)

            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_complete', order_id=order.id)
        else:
            if not shipping_form.is_valid():
                print(shipping_form.errors)
            messages.error(request, 'There was an error with your order. Please check the forms and try again.')
    else:
        shipping_form = ShippingAddressForm(prefix='shipping')
        payment_form = PaymentInfoForm(prefix='payment')

    return render(request, 'store/checkout.html', {
        'shipping_form': shipping_form,
        'payment_form': payment_form
    })


def order_complete(request, order_id):
    # Get the order
    order = get_object_or_404(Order, id=order_id)

    # Check that the order belongs to the user
    if order.user != request.user:
        return HttpResponseForbidden()

    context = {
        'order': order
    }

    return render(request, 'store/order_complete.html', context)
