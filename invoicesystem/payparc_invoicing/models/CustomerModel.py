from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class CustomerModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    company_number = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    zip = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    vat_country = models.CharField(max_length=100)
    vat_id = models.CharField(max_length=11)

    class Meta:
        db_table = 'customer'
        verbose_name = _('Customer')
