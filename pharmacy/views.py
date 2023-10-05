
from rest_framework import viewsets,status,permissions
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Product,Supplier,SaleItem, Sale,StockAlert,Stock,Patient,LabRequest,PatientNotes
from .serializers import ProductSerializer,LabRequestSerializer,PatientNotesSerializer,PatientSerializer,SupplierSerializer,StockSerializer,SaleItemSerializer,SaleSerializer,UserSerializer,CustomTokenObtainPairSerializer,UserUpdateSerializer


from django.db.models import Sum,Min, Max
from django.db.models.functions import TruncDate
from datetime import datetime,time
from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.utils.timezone import timedelta

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



class LabRequestViewSet(viewsets.ModelViewSet):
    queryset = LabRequest.objects.all()
    serializer_class = LabRequestSerializer
    permission_classes = [permissions.AllowAny]

class PatientNotesViewSet(viewsets.ModelViewSet):
    queryset = PatientNotes.objects.all()
    serializer_class = PatientNotesSerializer
    permission_classes = [permissions.AllowAny]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Use the custom serializer


@api_view(['POST'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    is_admin = request.data.get('is_admin', False)
    

    if not username or not password or not email :
        return Response({'error': 'Please provide username, email and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(username=username,email=email,first_name=first_name,last_name=last_name)
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

    def perform_update(self, serializer):
        instance = serializer.save()

        # Retrieve the associated StockAlert instance for this product
        try:
            stock_alert = StockAlert.objects.get(product=instance)
        except StockAlert.DoesNotExist:
            # If no StockAlert exists for this product, create one with default values
            stock_alert = StockAlert(product=instance)

        # Check if the product quantity is equal, less, or above the threshold
        if instance.quantity <= stock_alert.threshold:
            stock_alert.is_active = True
        else:
            stock_alert.is_active = False

        # Save the StockAlert instance
        stock_alert.save()

        # Your custom logic here
        # For example, you can update the captured timestamp or perform other actions
        # whenever a product is updated.

        # For instance, updating the captured timestamp:
        instance.captured = timezone.now()
        instance.save()


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
        if sale_serializer.validated_data['is_lab_bill']:
           pass
        else:
            for item_data in sale_items_data:
                product_id = item_data['product']
                quantity = item_data['quantity']
                print(quantity)
                product = Product.objects.get(pk=product_id)
                total_amount += product.price * quantity

            # Set total_amount in validated_data
            sale_serializer.validated_data['total_amount'] = total_amount

        # If it's a credit sale, set paid_amount to the posted value (if provided)
        # Otherwise, set it to total_amount
        
    
        if sale_serializer.validated_data['is_credit_sale']: 
            total_amount = request.data.get('total_amount')
            paid_amount = request.data.get('paid_amount', total_amount)
            sale_serializer.validated_data['paid_amount'] = paid_amount

        else:
            if sale_serializer.validated_data['is_lab_bill']:
                total_amount = request.data.get('total_amount')
                sale_serializer.validated_data['paid_amount'] = total_amount
            else:
                sale_serializer.validated_data['paid_amount'] = total_amount
            


        
       
        # Save the Sale instance
        sale = sale_serializer.save()

        # Save the SaleItem instances with a reference to the Sale
        if sale_serializer.validated_data['is_lab_bill']:
            pass
        else:
            for item_data in sale_items_data:
                print(item_data['quantity'])
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
    # Total Unpaid Credit from pharmacy sales to date


    result = Sale.objects.filter(is_credit_sale=True,is_lab_bill=False).aggregate(
        total_credit_sales=Sum(models.F('total_amount') - models.F('paid_amount')),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_credit_sales = result['total_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']



    # Return the result as JSON response
    response_data = {'total': total_credit_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_credit_sales_balance_lab(request):
    # Total Unpaid Credit from lab billing to 

    result = Sale.objects.filter(is_credit_sale=True,is_lab_bill=True).aggregate(
        total_credit_sales=Sum(models.F('total_amount') - models.F('paid_amount')),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_credit_sales = result['total_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

    # Return the result as JSON response
    response_data = {'total': total_credit_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_credit_sales_balance_today(request):
    # Total Unpaid Credit from pharmacy sales to date

    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(is_credit_sale=True,is_lab_bill=False,created__range=(start_of_day, end_of_day)).aggregate(
        total_credit_sales=Sum(models.F('total_amount') - models.F('paid_amount')),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_credit_sales = result['total_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']



    # Return the result as JSON response
    response_data = {'total': total_credit_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_credit_sales_balance_lab_today(request):
    # Total Unpaid Credit from lab billing to 
    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(is_credit_sale=True,is_lab_bill=True,created__range=(start_of_day, end_of_day)).aggregate(
        total_credit_sales=Sum(models.F('total_amount') - models.F('paid_amount')),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_credit_sales = result['total_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

    # Return the result as JSON response
    response_data = {'total': total_credit_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)




from django.utils import timezone

@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_non_credit_sales(request):
    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(
        is_lab_bill=False,
        created__range=(start_of_day, end_of_day)
    ).aggregate(
        total_non_credit_sales=Sum('paid_amount'),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_non_credit_sales = result['total_non_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

    # Return the result as JSON response
    response_data = {
        'total': total_non_credit_sales,
        'start_date': naturaltime(oldest_created_date),
        'end_date': naturaltime(latest_created_date)
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_non_credit_sales_lab(request):

    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(
        is_lab_bill=True,
        created__range=(start_of_day, end_of_day)
    ).aggregate(
        total_non_credit_sales=Sum('paid_amount'),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )


    total_non_credit_sales = result['total_non_credit_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

  

    # Return the result as JSON response
    response_data = {'total': total_non_credit_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_sales(request):
     # Daily total sales value Pharmacy

    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(
        is_lab_bill=False,
        created__range=(start_of_day, end_of_day)
    ).aggregate(
        total_sales=Sum('total_amount'),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )

    total_sales = result['total_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

    # Return the result as JSON response
    response_data = {'total': total_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def calculate_total_sale_lab(request):
    # Daily total sales value LAB

    today = timezone.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    result = Sale.objects.filter(
        is_lab_bill=True,
        created__range=(start_of_day, end_of_day)
    ).aggregate(
        total_sales=Sum('total_amount'),
        oldest_created_date=Min('created'),
        latest_created_date=Max('created')
    )
    total_sales = result['total_sales'] or 0.00
    oldest_created_date = result['oldest_created_date']
    latest_created_date = result['latest_created_date']

    # Return the result as JSON response
    response_data = {'total': total_sales,'start_date':naturaltime(oldest_created_date),'end_date':naturaltime(latest_created_date)}
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def all_captured_stock(request):
    stock = Stock.objects.all()
    response_data=[]
    for i in stock:
        stockitem = {'id':i.id,'quantity': i.quantity, 'receivedby':i.receivedby, 'purchase_price':i.purchase_price,'captured':naturaltime(i.captured), 'product':i.getProductName,'product_id':i.product.id}
        response_data.append(stockitem)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def credit_sales_summary(request):
    credit_sales = Sale.objects.filter(is_credit_sale=True,is_lab_bill=False).order_by('-created')
    response_data=[]
    for i in credit_sales:
        # if i.paid_amount != i.total_amount:
        if i.patient:
            sale = {'id':i.id,'unpaid':i.total_amount - i.paid_amount,'created':naturaltime(i.created),'total_amount': i.total_amount, 'paid_amount':i.paid_amount, 'customer':i.patient.getFullName, 'customer_number':i.patient.phone,'customer_location':i.patient.address, 'staff':i.user.getFullName}
            response_data.append(sale)
        else:
            sale = {'id':i.id,'unpaid':i.total_amount - i.paid_amount,'created':naturaltime(i.created),'total_amount': i.total_amount, 'paid_amount':i.paid_amount, 'customer':'Null', 'customer_number':'Null','customer_location':'Null', 'staff':i.user.getFullName}
            response_data.append(sale)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def cash_sales_summary(request):
    cash_sales = Sale.objects.filter(is_credit_sale=False,is_lab_bill=False).order_by('-created')
    response_data=[]
    for i in  cash_sales:
        if i.patient:
            sale = {'id':i.id,'created':naturaltime(i.created),'total_amount': i.total_amount,'customer':i.patient.getFullName, 'customer_number':i.patient.phone,'customer_location':i.patient.address, 'staff':i.user.getFullName}
            response_data.append(sale)
        else:
            sale = {'id':i.id,'created':naturaltime(i.created),'total_amount': i.total_amount,'customer':'Null', 'customer_number':'Null','customer_location':'Null', 'staff':i.user.getFullName}
            response_data.append(sale)
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def credit_sales_summary_lab(request):
    credit_sales = Sale.objects.filter(is_credit_sale=True,is_lab_bill=True).order_by('-created')
    response_data=[]
    for i in credit_sales:
        # if i.paid_amount != i.total_amount:
        if i.patient:
            sale = {'id':i.id,'unpaid':i.total_amount - i.paid_amount,'created':naturaltime(i.created),'total_amount': i.total_amount, 'paid_amount':i.paid_amount, 'customer':i.patient.getFullName, 'customer_number':i.patient.phone,'customer_location':i.patient.address, 'staff':i.user.getFullName}
            response_data.append(sale)
        else:
            sale = {'id':i.id,'unpaid':i.total_amount - i.paid_amount,'created':naturaltime(i.created),'total_amount': i.total_amount, 'paid_amount':i.paid_amount, 'customer':'Null', 'customer_number':'Null','customer_location':'Null', 'staff':i.user.getFullName}
            response_data.append(sale)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def cash_sales_summary_lab(request):
    cash_sales = Sale.objects.filter(is_credit_sale=False,is_lab_bill=True).order_by('-created')
    response_data=[]
    for i in  cash_sales:
        if i.patient:
            sale = {'id':i.id,'created':naturaltime(i.created),'total_amount': i.total_amount,'customer':i.patient.getFullName, 'customer_number':i.patient.phone,'customer_location':i.patient.address, 'staff':i.user.getFullName}
            response_data.append(sale)
        else:
            sale = {'id':i.id,'created':naturaltime(i.created),'total_amount': i.total_amount,'customer':'Null', 'customer_number':'Null','customer_location':'Null', 'staff':i.user.getFullName}
            response_data.append(sale)
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def sale_summary(request,pk):
    sale = Sale.objects.get(pk=pk)
    
    response = {
        'id':sale.id,
        'created':naturaltime(sale.created),
        'total_amount': sale.total_amount,
        'saleItems':sale.getSaleItems,
        'staff':sale.user.getFullName,
        'description':sale.lab_request_details
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def stock_alerts(request):
    stock_alerts = StockAlert.objects.filter(is_active=True)
    response=[]
    for i in stock_alerts:
        stockalert = {
            'id':i.id,
            'product':i.product.name,
            'product_id':i.product.id,
            'product_quantity':i.product.quantity,
        }
        response.append(stockalert)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def get_patient_notes(request,pk):
    patient_notes = PatientNotes.objects.filter(patient=pk)
    response=[]
    for i in patient_notes:
        notes = {
            'id':i.id,
            'notes':i.notes,
            'captured':naturaltime(i.captured),
         
        }
        response.append(notes)
    return Response(response, status=status.HTTP_200_OK)
