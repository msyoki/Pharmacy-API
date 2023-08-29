from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100)
    quantity_sold = models.PositiveIntegerField()
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()

class Debt(models.Model):
    customer = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

class Credit(models.Model):
    customer = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_date = models.DateField()
    due_date = models.DateField()
