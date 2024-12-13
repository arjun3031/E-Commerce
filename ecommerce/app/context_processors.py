# app/context_processors.py

from .models import Customer, Cart, CartItem

def cart_item_count(request):
    item_count = 0
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer)
            item_count = CartItem.objects.filter(cart=cart).count()  # Count all items in the cart
        except (Customer.DoesNotExist, Cart.DoesNotExist):
            item_count = 0
    return {'cart_item_count': item_count}
