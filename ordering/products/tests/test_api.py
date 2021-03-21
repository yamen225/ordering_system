from accounts.models import User
from model_mommy import mommy
from orders.models import Order
from rest_framework.test import APITestCase

from ..models import Product


class ProductApiTests(APITestCase):
    """Test Product View Set Endpoints
    """

    def setUp(self):
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.normal_user: User = User.objects.create(
            username='normal', password='1234', is_staff=False)
        self.products = mommy.make(Product, seller=self.admin_user, _quantity=5)
        [i.save() for i in self.products]
        self.product: Product = Product.objects.create(
            seller=self.admin_user, price=10, name="test product")

    def test_admin_can_get_all_products(self):
        self.client.force_authenticate(user=self.admin_user)

        res = self.client.get('/api/v1/products/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], Product.objects.count())
        self.assertTrue(any([i['is_deleted'] is False for i in res.data['results']]))

    def test_non_admin_cannot_get_all_products_only_available(self):
        prod1: Product = Product(seller=self.admin_user,price=10, is_deleted=True, name="wp")
        prod1.save()
        self.client.force_authenticate(user=self.normal_user)

        res = self.client.get('/api/v1/products/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'],
                         Product.objects.filter(is_deleted=False).count())
        self.assertFalse(any([i['name'] == 'wp' for i in res.data['results']]))
        self.assertTrue(all(
            [i['name'] in Product.get_available_products().values_list('name', flat=True)
             for i in res.data['results']]))

    def test_admin_can_create_product(self):
        prod_count = Product.objects.count()
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'name': 'test product'}

        res = self.client.post('/api/v1/products/', data, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(name='test product').exists())
        self.assertEqual(prod_count + 1, Product.objects.count())

    def test_admin_can_edit_product(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'name': 'test product'}
        res = self.client.post('/api/v1/products/', data, format='json')
        prod_count = Product.objects.count()
        data = {'price': 20, 'name': 'test product1'}

        res = self.client.put(
            '/api/v1/products/{}/'.format(res.data['id']), data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Product.objects.filter(name='test product1').exists())
        self.assertEqual(prod_count, Product.objects.count())

    def test_admin_can_delete_product(self):
        """Ensure admin can soft_delete an item"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'name': 'test product1'}
        res = self.client.post('/api/v1/products/', data, format='json')

        res = self.client.delete(
            '/api/v1/products/{}/'.format(res.data['id']), data, format='json')

        self.assertEqual(res.status_code, 204)
        self.assertTrue(Product.objects.get(name='test product1').is_deleted)

    def test_endpoint_returns_400_on_wrong_data(self):
        prod_count = Product.objects.count()
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': -20, 'name': 'test product'}

        res = self.client.post('/api/v1/products/', data, format='json')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(prod_count, Product.objects.count())

    def test_normal_user_can_get_purchased_products(self):
        Order.objects.all().delete()

        orders = mommy.make(
            Order, buyer=self.normal_user, product=self.product,
            amount=self.product.price, _quantity=3)
        [i.save() for i in orders]

        self.client.force_authenticate(user=self.normal_user)

        res = self.client.get('/api/v1/products/purchased/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'],
                         Product.objects.filter(orders__buyer=self.normal_user).count())
        self.assertTrue(any([i['name'] == 'test product' for i in res.data['results']]))
        self.assertTrue(all(
            [i['name'] in Product.get_all_purchased(
                user=self.normal_user).values_list('name', flat=True)
             for i in res.data['results']]))

    def test_admin_cannot_create_order(self):
        self.client.force_authenticate(user=self.admin_user)

        res = self.client.get('/api/v1/products/purchased/')

        self.assertEqual(res.status_code, 403)
