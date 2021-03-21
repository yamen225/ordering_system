from django.test import TestCase

from accounts.models import User
from model_mommy import mommy
from orders.models import Order

from ..models import Product


class ProductTest(TestCase):
    """Test Product Mode
    """

    def setUp(self):
        self.admin_user: User = User.objects.create(
            username='admin', password='1234', is_staff=True)
        self.normal_user: User = User.objects.create(
            username='non_admin', password='1234', is_staff=False)
        self.product: Product = Product.objects.create(
            seller=self.admin_user, price=10, name="test product")
        super().setUp()

    def test_seller_can_not_be_non_admin(self):
        """will not save if product seller is not admin
        """
        prod_count = Product.objects.count()
        p = Product(
            seller=self.normal_user, price=1, name="prod 1")
        self.assertFalse(p.save())
        self.assertEqual(prod_count, Product.objects.count())

    def test_seller_can_only_be_admin(self):
        """will save if product seller is admin
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.admin_user, price=1, name="prod 1")
        self.assertNotEqual(prod_count, Product.objects.count())

    def test_price_must_be_gt_0(self):
        """will not save if product price is less than 1
        """
        prod_count = Product.objects.count()
        p = Product.objects.create(
            seller=self.normal_user, price=0, name="prod 1")
        self.assertEqual(prod_count, Product.objects.count())


    def test_can_get_products_purchased_by_user(self):
        Order.objects.all().delete()

        orders = mommy.make(
            Order, buyer=self.normal_user, product=self.product,
            amount=self.product.price, _quantity=3)
        [i.save() for i in orders]

        other_user: User = User.objects.create(
            username='other', password='1234', is_staff=False)
        prod1 = Product(seller=self.admin_user, price=10, name="wp")
        prod1.save()

        other_orders = mommy.make(
            Order, buyer=other_user, product=prod1,
            amount=self.product.price, _quantity=3)
        [i.save() for i in other_orders]

        self.assertTrue(Product.get_all_purchased(
            user=self.normal_user),
            Product.objects.filter(id=self.product.id))
        self.assertTrue(Product.get_all_purchased(
            user=other_user),
            Product.objects.filter(id=prod1.id))