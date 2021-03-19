from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Product (models.Model):
    """Products Model"""
    seller = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='products',
        help_text='creator of product from user model - must be admin')
    price = models.FloatField(
        validators=[MinValueValidator(1)],
        help_text='price of product in EUR - must be gt 0')
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='number of items available from this product to be sold - must be gte 0'
    )
    name = models.CharField(max_length=255, help_text='product name')

    def save(self, *args, **kwargs):
        """override save function to ensure seller.is_admin is True
        """
        if not self.seller.is_staff or self.quantity < 0 or self.price <= 0:
            return False
        super().save(*args, **kwargs)
