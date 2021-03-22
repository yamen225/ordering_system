from django.core.validators import MinValueValidator
from django.db import models
from currencies.models import Currency
# Create your models here.


class Product (models.Model):
    """Products Model"""
    seller = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='products',
        help_text='creator of product from user model - must be admin')
    price = models.FloatField(
        validators=[MinValueValidator(1)],
        help_text='price of product in chosen currency - must be gt 0')
    name = models.CharField(max_length=255, help_text='product name')
    is_deleted = models.BooleanField(default=False)
    currency = models.ForeignKey(
        'currencies.Currency', on_delete=models.CASCADE, related_name='products',
        help_text='currency of the product')

    def save(self, *args, **kwargs):
        """override save function to ensure validations
        """
        if not self.seller.is_staff or self.price <= 0:
            return False
        super().save(*args, **kwargs)

    @staticmethod
    def get_available_products(user):
        qs = Product.objects.filter(is_deleted=False)
        user_currency = user.currency
        print(user_currency)
        if user_currency:
            Currency.updating_latest_values()
            user_currency_current_value = Currency.objects.get(id=user_currency.id).value
            print(user_currency_current_value)
            qs = qs.annotate(
                user_currency_price=(models.F('price') / models.F('currency__value')
                                     ) * user_currency_current_value)
        return qs

    @staticmethod
    def get_all_purchased(user):
        return Product.objects.filter(orders__buyer=user)