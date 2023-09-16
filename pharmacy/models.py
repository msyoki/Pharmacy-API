from django.db import models


# api/models.py
# customuser/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,first_name,last_name, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,first_name,last_name, password=None):
        user = self.create_user(username,email,first_name,last_name,password)
        user.is_admin = True
        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
        return self.username



class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

# class SubCategory(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
 
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField()
    expirydate = models.DateField()
    captured = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    # subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        is_new_product = self.pk is None  # Check if it's a new product
        super().save(*args, **kwargs)
        
        # Create a StockAlert instance only for new products
        if is_new_product:
            StockAlert.objects.create(product=self)

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    receivedby = models.CharField(max_length=100)
    captured = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Get the product original quantity and update it based on the sale item quantity
        original_quantity = self.product.quantity
        self.product.quantity = original_quantity + self.quantity
        self.product.save()

        # Update the stock alert
        stock_alert = StockAlert.objects.get(product=self.product)

        # Check if the quantity is below or equal to the threshold and take action if needed
        if self.product.quantity <= stock_alert.threshold and not stock_alert.is_active:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = True
            stock_alert.save()
        elif self.product.quantity > stock_alert.threshold and stock_alert.is_active:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = False
            stock_alert.save()

        super(Stock, self).save(*args, **kwargs)

    @property
    def getProductName(self):
        product = Product.objects.get(pk=self.product.id)
        return product.name


class StockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    threshold = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=False)

    def check_and_alert(self):
        if self.is_active and self.product.quantity <= self.threshold:
            # Here you can implement your alert mechanism, such as sending notifications
            alert_message = f"ALERT: Product '{self.product.name}' is low in stock (current quantity: {self.product.quantity})"
            print(alert_message)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.check_and_alert()

class Sale(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    is_credit_sale = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    customer = models.CharField(max_length=100,blank=True)
    customer_number = models.CharField(max_length=100,blank=True)
    customer_location = models.CharField(max_length=100,blank=True)


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    birth_cerificate_or_id = models.CharField(max_length=100,unique=True)
    dob = models.DateField()
    address = models.CharField(max_length=100)


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Get the product original quantity and update it based on the sale item quantity
        original_quantity = self.product.quantity
        self.product.quantity = original_quantity - self.quantity
        self.product.save()

        # Update the stock alert
        stock_alert = StockAlert.objects.get(product=self.product)

        # Check if the quantity is below or equal to the threshold and take action if needed
        if self.product.quantity <= stock_alert.threshold and not stock_alert.is_active:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = True
            stock_alert.save()
        elif self.product.quantity > stock_alert.threshold and stock_alert.is_active:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = False
            stock_alert.save()

        super(SaleItem, self).save(*args, **kwargs)
