from rest_framework import serializers
from .models import Product, CreditSale,CashSale,Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    suppliers = SupplierSerializer(many=True)  # Many-to-many relationship

    class Meta:
        model = Product
        fields = '__all__'


class CreditSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditSale
        fields = '__all__'

class CashSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSale
        fields = '__all__'

