from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StoreViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Audio', slug='audio', icon='fa-headphones')
        self.product = Product.objects.create(
            name='Studio Headphones',
            slug='studio-headphones',
            category=self.category,
            brand='SoundLab',
            description='Comfortable wireless headphones for focused listening.',
            price='199.99',
            is_featured=True,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Studio Headphones')

    def test_product_list_loads(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Studio Headphones')

    def test_search_filters_products(self):
        response = self.client.get(reverse('store:product_list'), {'q': 'soundlab'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Studio Headphones')

    def test_category_filter_filters_products(self):
        response = self.client.get(reverse('store:product_list'), {'category': 'audio'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Studio Headphones')

    def test_customer_can_add_product_to_cart(self):
        response = self.client.post(
            reverse('store:cart_add', args=[self.product.pk]),
            {'next': reverse('store:product_list')},
        )
        self.assertRedirects(response, reverse('store:product_list'))
        cart_response = self.client.get(reverse('store:cart_detail'))
        self.assertContains(cart_response, 'Studio Headphones')
        self.assertContains(cart_response, '199.99')

    def test_customer_can_update_and_remove_cart_item(self):
        self.client.post(reverse('store:cart_add', args=[self.product.pk]))
        cart_response = self.client.get(reverse('store:cart_detail'))
        item = cart_response.context['items'][0]
        self.client.post(reverse('store:cart_update', args=[item.pk]), {'quantity': 2})
        cart_response = self.client.get(reverse('store:cart_detail'))
        self.assertContains(cart_response, '399.98')
        self.client.post(reverse('store:cart_remove', args=[item.pk]))
        cart_response = self.client.get(reverse('store:cart_detail'))
        self.assertContains(cart_response, 'Your cart is empty')
