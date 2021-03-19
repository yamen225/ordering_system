from django.test import TestCase

from accounts.models import User
from ..models import Product


class ProductTest(TestCase):
    """Test Product Mode
    """

    def setUp(self):
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.normal_user: User = User.objects.create(
            username='non_admin', password='1234', is_staff=False)
        super().setUp()

    def test_seller_can_not_be_non_admin(self):
        """will not save if product seller is not admin
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.normal_user, price=1, quantity=1, name="prod 1")
        self.assertEqual(prod_count, Product.objects.count())

    def test_seller_can_only_be_admin(self):
        """will not save if product seller is not admin
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.admin_user, price=1, quantity=1, name="prod 1")
        self.assertNotEqual(prod_count, Product.objects.count())

    def test_quantity_must_be_gte_0(self):
        """will not save if product quantity is less than zero
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.admin_user, price=1, quantity=-1, name="prod 1")
        self.assertEqual(prod_count, Product.objects.count())

    def test_price_must_be_gt_0(self):
        """will not save if product price is less than 1
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.normal_user, price=0, quantity=1, name="prod 1")
        self.assertEqual(prod_count, Product.objects.count())
