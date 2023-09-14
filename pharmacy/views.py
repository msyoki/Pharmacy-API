
from rest_framework import viewsets,status,permissions
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Product,Supplier,SaleItem, Sale,StockAlert,Stock
from .serializers import ProductSerializer,SupplierSerializer,StockSerializer,SaleItemSerializer,SaleSerializer,UserSerializer,CustomTokenObtainPairSerializer,UserUpdateSerializer


from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import datetime
from django.db import models

CustomUser = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    # http_method_names = ['get']

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Use the custom serializer


@api_view(['POST'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def register_user(request):
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    is_admin = request.data.get('is_admin', False)

    if not password or not email:
        return Response({'error': 'Please provide email and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(email=email,first_name=first_name,last_name=last_name)
    if created:
        user.set_password(password)
        user.is_admin = is_admin  # Set the is_admin field
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user making the request
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Allow partial updates (including password)
        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-created') 
    serializer_class = SaleSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Serialize the Sale data
        sale_serializer = self.get_serializer(data=request.data)
        sale_serializer.is_valid(raise_exception=True)

        # Serialize the SaleItem data
        sale_items_data = request.data.get('sale_items', [])
        sale_items_serializer = SaleItemSerializer(data=sale_items_data, many=True)
        sale_items_serializer.is_valid(raise_exception=True)

        # Calculate total_amount based on SaleItem prices
        total_amount = 0
        for item_data in sale_items_data:
            product_id = item_data['product']
            quantity = item_data['quantity']
            product = Product.objects.get(pk=product_id)
            total_amount += product.price * quantity

        # Set total_amount in validated_data
        sale_serializer.validated_data['total_amount'] = total_amount

        # If it's a credit sale, set paid_amount to the posted value (if provided)
        # Otherwise, set it to total_amount
        if sale_serializer.validated_data['is_credit_sale']:
            paid_amount = request.data.get('paid_amount', total_amount)
        else:
            paid_amount = total_amount

        sale_serializer.validated_data['paid_amount'] = paid_amount

        # Save the Sale instance
        sale = sale_serializer.save()

        # Save the SaleItem instances with a reference to the Sale
        for item_data in sale_items_data:
            SaleItem.objects.create(
                product_id=item_data['product'],
                quantity=item_data['quantity'],
                sale=sale
            )

        headers = self.get_success_headers(sale_serializer.data)
        return Response(sale_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_daily_sales_total(request):
    # Get today's date
    today = datetime.now().date()

    # Query the database to calculate daily sales totals
    daily_sales = Sale.objects.filter(
      
    ).annotate(
        date=TruncDate('created')
    ).values(
        'date'
    ).annotate(
        total=Sum('total_amount')
    ).order_by(
        'date'
    )

    # Format the results into the desired list format
    results = [{'date': sale['date'], 'total': sale['total']} for sale in daily_sales]

    return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_credit_sales_balance(request):
    # Calculate the sum of total_amount - paid_amount for credit sales
    credit_sales_balance = Sale.objects.filter(is_credit_sale=True).aggregate(
        credit_sales_balance=Sum(models.F('total_amount') - models.F('paid_amount'))
    )['credit_sales_balance'] or 0.00

    # Return the result as JSON response
    response_data = {'total': credit_sales_balance}
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_non_credit_sales(request):
    # Calculate the total of total_amount for non-credit sales
    total_non_credit_sales = Sale.objects.all().aggregate(
        total_non_credit_sales=Sum('paid_amount')
    )['total_non_credit_sales'] or 0.00

    # Return the result as JSON response
    response_data = {'total': total_non_credit_sales}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_sales(request):
    # Calculate the total of total_amount for non-credit sales
    total_sales = Sale.objects.all().aggregate(
        total_sales=Sum('total_amount')
    )['total_sales'] or 0.00

    # Return the result as JSON response
    response_data = {'total': total_sales}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def all_captured_stock(request):
    stock = Stock.objects.all()
    response_data=[]
    for i in stock:
        stockitem = {'id':i.id,'quantity': i.quantity, 'receivedby':i.receivedby, 'captured':i.captured, 'product':i.getProductName}
        response_data.append(stockitem)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def credit_sales_summary(request):
    credit_sales = Sale.objects.filter(is_credit_sale=True)
    response_data=[]
    for i in credit_sales:
        if i.paid_amount != i.total_amount:
            sale = {'id':i.id,'unpaid':i.total_amount - i.paid_amount,'created':i.created,'total_amount': i.total_amount, 'paid_amount':i.paid_amount, 'customer':i.customer, 'customer_number':i.customer_number,'customer_location':i.customer_location}
            response_data.append(sale)
    return Response(response_data, status=status.HTTP_200_OK)
