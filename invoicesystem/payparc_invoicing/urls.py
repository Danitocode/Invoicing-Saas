from django.urls import path
from .views import get_invoice_template, post_item, get_invoice, get_all_invoices, \
    get_all_customers, get_all_items, post_customer

app_name = 'payparc_invoicing'

urlpatterns = [
    # GET methods
    path('invoice/template/<int:pk>/', get_invoice_template, name='invoice-template'),
    path('invoice/<int:pk>/', get_invoice, name='invoice-json'),
    path('invoice/all/', get_all_invoices, name='all-invoice-json'),
    path('invoice/customers/', get_all_customers, name='all-invoice-json'),
    path('invoice/items/', get_all_items, name='all-invoice-json'),
    # POST methods
    path('invoice/item/', post_item, name='invoice-item'),
    path('invoice/customer/', post_customer, name='customer'),
]
