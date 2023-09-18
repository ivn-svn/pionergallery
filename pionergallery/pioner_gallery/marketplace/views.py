from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pioner_gallery.user_login.models import UserPhoto
from pioner_gallery.marketplace.models import Cart, CartItem
from django.shortcuts import redirect
from django.db.models import Q
from pioner_gallery.braintree_config import gateway
from django.http import JsonResponse


def process_payment(request):
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)

        # Log the received nonce
        print(f"Received nonce: {nonce}")

        if not nonce:
            return JsonResponse({"error": "Nonce not received."})

        # Use the nonce with your Braintree gateway to process the payment
        result = gateway.transaction.sale({
            "amount": "10.00",  # Example amount, adjust accordingly
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            return JsonResponse({"success": True})
        else:
            # Enhanced error handling
            error_messages = []
            for error in result.errors.deep_errors:
                error_messages.append(f"Error code: {error.code}. Error message: {error.message}")
            return JsonResponse({"success": False, "errors": error_messages})

    return JsonResponse({"error": "Invalid request."})


def all_products(request):
    products = UserPhoto.objects.all()
    return render(request, 'pioner_gallery/orders.html', {'products': products})


def dashboard_view(request):
    return render(request, 'pioner_gallery/marketplace_dashboard.html')


def checkout_view(request):
    client_token = gateway.client_token.generate()  # Assuming 'gateway' has been initialized as shown previously
    context = {
        'client_token': client_token,
        # ... other context variables ...
    }
    return render(request, 'shop/checkout/index.html', context)


def products_view(request):
    # products = UserPhoto.objects.all()

    query = request.GET.get('query', '')
    products = UserPhoto.objects.filter(
        Q(photo_name__icontains=query) |
        Q(category__icontains=query) |
        Q(subcategory__icontains=query) |
        Q(description__icontains=query) |
        Q(price__icontains=query)
    )
    print(products)
    context = {
        'products': products
    }
    return render(request, 'pioner_gallery/products.html', context)


@login_required
def add_to_cart(request):
    if request.method == "POST":
        photo_id = request.POST.get('photo_id')
        photo = UserPhoto.objects.get(id=photo_id)

        # Check if the user has a cart, if not, create one
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # Add the photo to the cart or update its quantity
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, photo=photo)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_items = CartItem.objects.filter(cart=user_cart)

    else:  # If direct GET request to add_to_cart URL, just show the cart
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=user_cart)
        except Cart.DoesNotExist:
            cart_items = []
    try:
        user_cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        total_quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_quantity = 0
    total_price = sum(item.photo.price for item in cart_items)

    return render(request, 'pioner_gallery/orders.html',
                  {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price})


def remove_from_cart(request, item_id):
    # Assuming you have a Cart model and CartItem model
    cart = Cart.objects.get(user=request.user)  # adjust this if your retrieval method is different
    item_to_remove = cart.items.get(id=item_id)
    item_to_remove.delete()
    return redirect('add_to_cart')
