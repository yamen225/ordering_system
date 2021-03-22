from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    """Store Order"""

    product = models.ForeignKey(
        'products.Product', on_delete=models.DO_NOTHING, related_name='orders',
        help_text='Product id being purchased')
    buyer = models.ForeignKey(
        'accounts.User', on_delete=models.DO_NOTHING, related_name='bought',
        help_text='buyer of order from user model - must not be admin')
    amount = models.FloatField(
        validators=[MinValueValidator(1)],
        help_text='order amount in buyer currency - must be gt 0 and equal to product price')

    def save(self, *args, **kwargs):
        """override save function to ensure validations
        """
        if self.buyer.is_staff or self.product.is_deleted:
            return False
        self.product.save()
        super().save(*args, **kwargs)

    @staticmethod
    def get_sum_purchased() -> float:
        """return the sum of all purchased products"""
        return Order.objects.all().aggregate(
            models.Sum('product__price'))['product__sum'] or 0.00
