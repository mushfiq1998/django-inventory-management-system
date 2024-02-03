from django.contrib import admin
from . import models

admin.site.register(models.Vendor)
admin.site.register(models.Unit)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_mobile']
    search_fields = ['customer_name', 'customer_mobile']
admin.site.register(models.Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit']
    search_fields = ['title', 'unit__title']
admin.site.register(models.Product, ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'quantity', 'price', 
    'vendor', 'purchase_date']
    search_fields = ['product__title']
admin.site.register(models.Purchase, PurchaseAdmin)

class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'price', 
    'total_amount', 'sale_date']
    search_fields = ['product__title']
admin.site.register(models.Sale, SaleAdmin)

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__unit__title']
    list_display = ['product', 'purchase_quantity', 'sale_quantity', 
    'total_balance_quantity', 'product_unit', 'purchase_date', 
    'sale_date', 'vendor', 'customer']
admin.site.register(models.Inventory, InventoryAdmin)
 