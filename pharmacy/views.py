from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Product,Supplier, Sale,Category,SubCategory,StockAlert
from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer,SupplierSerializer, SaleSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product_name = request.data.get('name')

        if Product.objects.filter(name=product_name).exists():
            return Response(
                {"error": "A product with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Get the original quantity before updating
        original_quantity = instance.quantity

        self.perform_update(serializer)

        # Get the updated quantity after updating
        updated_quantity = serializer.validated_data.get('quantity')

        # Get the stockalert instance
        stock_alert= StockAlert.objects.get(product=instance)

        # Check if the quantity has changed and take action if needed
        if updated_quantity > stock_alert.threshold:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = False
            stock_alert.save()

           
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
