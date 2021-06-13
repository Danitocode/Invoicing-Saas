from django.db import models
from ..models import CustomerModel
from django.utils.translation import ugettext_lazy as _
from .TimestampedModel import TimestampedModel


class InvoiceType(models.TextChoices):
    PROFORMA = 'PROFORMA'
    INTERIM = 'INTERIM'
    COLLECTIVE = 'COLLECTIVE'
    FINAL = 'FINAL'
    RECURRING = 'RECURRING'


class InvoiceState(models.TextChoices):
    ISSUED = 'ISSUED'
    DRAFT = 'DRAFT'
    PAID = 'PAID'


class Currency(models.TextChoices):
    Romania = 'RON'
    Russia = 'RUB'
    Nicaragua = 'NIO'
    Canada = 'CAD'
    United_States = 'USD'
    Spain = 'EUR'


class InvoiceModel(TimestampedModel):
    company = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    invoice_type = models.CharField(max_length=12, choices=InvoiceType.choices,)
    invoice_state = models.CharField(max_length=10, choices=InvoiceState.choices,)
    currency = models.CharField(max_length=13, choices=Currency.choices,)

    class Meta:
        db_table = 'invoice'
        verbose_name = _('Invoice')


class InvoiceItemsModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit_price = models.FloatField()

    class Meta:
        db_table = 'invoice_item'
        verbose_name = _('Invoice item')