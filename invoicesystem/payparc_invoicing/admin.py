from django.contrib import admin
from .models import CustomerModel, InvoiceModel, InvoiceItemsModel

admin.site.register(CustomerModel)
admin.site.register(InvoiceModel)
admin.site.register(InvoiceItemsModel)
