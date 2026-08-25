from .models import Cart


def cart_context(request):
    """Expose the current session cart count without creating empty carts."""
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return {'cart_count': 0}

    try:
        cart = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist:
        request.session.pop('cart_id', None)
        return {'cart_count': 0}

    return {'cart_count': sum(item.quantity for item in cart.items.all())}
