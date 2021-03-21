from accounts.models import User
from model_mommy import mommy
from products.models import Product
from rest_framework.test import APITestCase

from ..models import Order
from currencies.models import Currency


class OrderApiTest(APITestCase):
    """Test Order API viewset
    """
    def setUp(self):
        self.normal_user: User = User.objects.create(
            username='normal', password='1234', is_staff=False)
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.currency = Currency.objects.first()
        self.product: Product = Product.objects.create(
            seller=self.admin_user, price=10, name="test product", currency=self.currency)


    def test_nomral_user_can_create_order(self):
        ord_count = Order.objects.count()
        self.client.force_authenticate(user=self.normal_user)
        order_data = {'amount': 20, 'product': self.product.id, 'currency': self.currency.id}

        ord_res = self.client.post('/api/v1/orders/', order_data, format='json')

        self.assertEqual(ord_res.status_code, 201)
        self.assertTrue(Order.objects.filter(amount=20).exists())
        self.assertNotEqual(ord_count, Order.objects.count())
        self.assertEqual(ord_res.data['product'], self.product.id)

    def test_admin_cannot_create_order(self):
        self.client.force_authenticate(user=self.admin_user)
        order_data = {'amount': 20, 'product': self.product.id, 'currency': self.currency.id}

        ord_res = self.client.post('/api/v1/orders/', order_data, format='json')

        self.assertEqual(ord_res.status_code, 405)

    def test_non_admin_cannot_get_revenue(self):
        self.client.force_authenticate(user=self.normal_user)

        ord_res = self.client.get('/api/v1/orders/total_revenue/', format='json')

        self.assertEqual(ord_res.status_code, 403)

    def test_admin_can_get_sum_of_orders_amount(self):
        Order.objects.all().delete()

        orders = mommy.make(
            Order, buyer=self.normal_user, product=self.product,
            amount=self.product.price, _quantity=3)
        [i.save() for i in orders]
        self.client.force_authenticate(user=self.admin_user)

        ord_res = self.client.get('/api/v1/orders/total_revenue/', format='json')
        self.assertEqual(ord_res.status_code, 200)
        self.assertTrue(ord_res.data['total_revenue'], self.product.price * 3)
