from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.db.models import Q
from .models import Cart, CartItem, Category, Product


def _get_cart(request, create=False):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            return Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            request.session.pop('cart_id', None)
    if create:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.pk
        return cart
    return None

class HomeView(TemplateView):
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use one ordered set of categories for consistent navigation and cards.
        categories = Category.objects.all().order_by('name')
        context['categories'] = categories[:4]
        context['nav_categories'] = categories[:5]
        
        # Featured products
        context['featured_products'] = Product.objects.filter(is_featured=True)[:3]
        
        # On sale products
        context['sale_products'] = Product.objects.filter(is_on_sale=True)[:4]
        
        # Top rated products
        context['top_rated_products'] = Product.objects.filter(is_top_rated=True)[:3]
        
        # Recently added products
        context['recent_products'] = Product.objects.order_by('-created_at')[:5]
        
        # Best sellers (using featured as best sellers for demo)
        context['best_sellers'] = Product.objects.filter(is_featured=True)[:4]
        
        # Special offer product
        context['special_offer'] = Product.objects.filter(is_on_sale=True).first()
        
        # Contact info
        context['contact_phone'] = '0594421734'
        context['store_name'] = 'Expensive Electronics'
        
        return context

def product_list(request):
    query = request.GET.get('q', '').strip()
    active_category = request.GET.get('category', '').strip()
    products = Product.objects.select_related('category').order_by('-created_at')

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(description__icontains=query)
        )
    if active_category:
        products = products.filter(category__slug=active_category)
    if request.GET.get('sale'):
        products = products.filter(is_on_sale=True)

    categories = Category.objects.all().order_by('name')
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'nav_categories': categories[:5],
        'active_category': active_category,
        'query': query,
        'contact_phone': '0594421734',
    })


def cart_detail(request):
    cart = _get_cart(request)
    items = list(cart.items.select_related('product') if cart else [])
    for item in items:
        item.line_total = item.product.price * item.quantity
    subtotal = sum(item.line_total for item in items)
    return render(request, 'store/cart.html', {
        'items': items,
        'subtotal': subtotal,
        'contact_phone': '0594421734',
    })


def cart_add(request, product_id):
    if request.method != 'POST':
        return redirect('store:product_list')

    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request, create=True)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save(update_fields=['quantity'])
    messages.success(request, f'{product.name} added to your cart.')
    return redirect(request.POST.get('next') or 'store:cart_detail')


def cart_update(request, item_id):
    if request.method != 'POST':
        return redirect('store:cart_detail')

    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = min(quantity, 99)
        item.save(update_fields=['quantity'])
    return redirect('store:cart_detail')


def cart_remove(request, item_id):
    if request.method == 'POST':
        cart = _get_cart(request)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.delete()
    return redirect('store:cart_detail')
