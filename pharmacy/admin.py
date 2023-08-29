from django.contrib import admin
from .models import Product, CreditSale,CashSale,Supplier

# Register your models here.

@admin.register(CreditSale)
class CreditSaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity_sold', 'sale_amount', 'sale_date')

@admin.register(CashSale)
class CashSaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity_sold', 'sale_amount', 'sale_date')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'price', 'display_suppliers')
    list_filter = ('suppliers',)

    def display_suppliers(self, obj):
        return ", ".join([supplier.name for supplier in obj.suppliers.all()])

    display_suppliers.short_description = 'Suppliers'
