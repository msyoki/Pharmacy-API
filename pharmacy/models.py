from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
 
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
   

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    is_credit_sale = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.product.price * self.quantity

        # Reduce the product quantity when a sale is created
        if self.pk is None:  # This checks if it's a new sale
            self.product.quantity -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)
