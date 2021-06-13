from rest_framework.serializers import ModelSerializer
from .models import InvoiceModel, InvoiceItemsModel, CustomerModel


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = InvoiceModel
        fields = '__all__'


class ItemSerializer(ModelSerializer):
    class Meta:
        model = InvoiceItemsModel
        fields = '__all__'


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = '__all__'
