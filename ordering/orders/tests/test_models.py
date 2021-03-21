from django.test import TestCase

from accounts.models import User
from model_mommy import mommy
from products.models import Product

from ..models import Order


class OrderTest(TestCase):
    """Test Order Mode
    """

    def setUp(self):
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.normal_user: User = User.objects.create(
            username='non_admin', password='1234', is_staff=False)
        self.product: Product = Product.objects.create(
            seller=self.admin_user, price=10, name="test product")
        super().setUp()

    def test_buyer_can_not_be_admin(self):
        """will not save order if product buyer is not admin
        """
        ord_count: int = Order.objects.count()
        o = Order(product=self.product,
                  buyer=self.admin_user, amount=self.product.price)
        self.assertFalse(o.save())
        self.assertEqual(ord_count, Order.objects.count())

    def test_product_cant_be_deleted(self):
        """will not save order if product is soft deleted
        """
        prod1: Product = Product(seller=self.admin_user, price=10, is_deleted=True, name="wp")
        prod1.save()
        ord_count: int = Order.objects.count()
        o = Order(product=prod1,
                  buyer=self.normal_user, amount=self.product.price)
        self.assertFalse(o.save())
        self.assertEqual(ord_count, Order.objects.count())

    def test_can_create_order(self):
        """will save order 
        """
        ord_count: int = Order.objects.count()
        o = Order(product=self.product, buyer=self.normal_user,
                  amount=self.product.price)
        o.save()
        self.assertEqual(ord_count + 1, Order.objects.count())

    def test_can_get_sum_of_all_purchased_orders(self):
        Order.objects.all().delete()
        orders = mommy.make(
            Order, buyer=self.normal_user, product=self.product,
            amount=self.product.price, _quantity=3)
        [i.save() for i in orders]

        self.assertEqual(Order.get_sum_purchased(), self.product.price * 3)

