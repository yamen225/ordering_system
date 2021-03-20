from rest_framework.test import APITestCase
from model_mommy import mommy
from accounts.models import User
from ..models import Product


class ProductApiTests(APITestCase):
    """Test Product View Set Endpoints
    """

    def setUp(self):
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.products = mommy.make(Product, seller=self.admin_user, _quantity=5)
        [i.save() for i in self.products]

    def test_admin_can_get_all_products(self):
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.get('/api/v1/products/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], Product.objects.count())

    def test_admin_can_create_product(self):
        prod_count = Product.objects.count()
        self.client.force_authenticate(user=self.admin_user)

        data = {'price': 20, 'quantity': 5, 'name': 'test product'}

        res = self.client.post('/api/v1/products/', data, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(name='test product').exists())
        self.assertEqual(prod_count + 1, Product.objects.count())

    def test_admin_can_edit_product(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'quantity': 5, 'name': 'test product'}
        res = self.client.post('/api/v1/products/', data, format='json')
        prod_count = Product.objects.count()
        data = {'price': 20, 'quantity': 5, 'name': 'test product1'}

        res = self.client.put(
            '/api/v1/products/{}/'.format(res.data['id']), data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Product.objects.filter(name='test product1').exists())
        self.assertEqual(prod_count, Product.objects.count())

    def test_admin_can_delete_product(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'quantity': 5, 'name': 'test product'}
        res = self.client.post('/api/v1/products/', data, format='json')
        prod_count = Product.objects.count()

        res = self.client.delete(
            '/api/v1/products/{}/'.format(res.data['id']), data, format='json')

        self.assertEqual(res.status_code, 204)
        self.assertFalse(Product.objects.filter(name='test product1').exists())
        self.assertEqual(prod_count - 1, Product.objects.count())

    def test_endpoint_returns_400_on_wrong_data(self):
        prod_count = Product.objects.count()
        self.client.force_authenticate(user=self.admin_user)
        data = {'price': 20, 'quantity': -5, 'name': 'test product'}

        res = self.client.post('/api/v1/products/', data, format='json')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(prod_count, Product.objects.count())
