import os
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import CustomerModel, InvoiceItemsModel, InvoiceModel
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .serializers import InvoiceSerializer, ItemSerializer, CustomerSerializer


# METHODS DECLARATION
# GET methods

# One item
@api_view(['GET'])
def get_invoice(request, pk):
    invoice = InvoiceModel.objects.get(id=pk)
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)


# All items
@api_view(['GET'])
def get_all_invoices(request):
    invoices = InvoiceModel.objects.all().order_by('-id')
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_customers(request):
    customers = CustomerModel.objects.all().order_by('-id')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_items(request):
    items = InvoiceItemsModel.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_item(request):
    serializer = ItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def post_customer(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# TEMPLATE CODE
class InvoiceListView(ListView):
    model = InvoiceModel
    template_name = 'invoice.html'


# In order to have images in the template, is necesary to have a path request
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


# Method for rendering the pdf
@api_view(['GET'])
def get_invoice_template(request, *args, **kwargs):
    pk = kwargs.get('pk')
    invoice = get_object_or_404(InvoiceModel, pk=pk)
    items = InvoiceItemsModel.objects.filter(invoice_id=pk)
    customer = CustomerModel.objects.get(pk=invoice.company_id)

    # Functions for making available mathematics operations
    def arithmetic_item_list():
        # Arithmetic operations for calculated fields
        item_list = []
        for item in items:
            # item_amount = str(item.unit_price)
            item_list.append(float(item.unit_price))
        return item_list

    item_list = arithmetic_item_list()

    def arithmetic_total_amount(item_list):
        # Arithmetic operations for calculated fields
        total_amount = sum(item_list)
        return total_amount

    total_amount = arithmetic_total_amount(item_list)

    def arithmetic_amount_iva(total_amount):
        # Arithmetic operations for calculated fields
        amount_iva = (total_amount * 0.21)
        return amount_iva

    amount_iva = arithmetic_amount_iva(total_amount)

    def arithmetic_final_amount(total_amount):
        # Arithmetic operations for calculated fields
        final_amount = (total_amount * 0.21) + total_amount
        return final_amount

    final_amount = arithmetic_final_amount(total_amount)

    template_path = 'invoice.html'

    # Model declaration as variables
    context = {'invoice': invoice, 'customer': customer, 'items': items, 'total_amount': total_amount,
               'amount_iva': amount_iva, 'final_amount': final_amount}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # If download:
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # Create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
