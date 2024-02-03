from django.db import models

class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="vendor")
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField()

    class Meta:
        verbose_name_plural = '1. Vendors'

    def __str__(self):
        return self.full_name

class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = '2. Units'

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="product/")

    class Meta:
        verbose_name_plural = '3. Products'

    def __str__(self):
        return self.title

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False, default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Purchases'
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super(Purchase, self).save(*args, **kwargs)

        # Update inventory effect related to purchase
        inventory = Inventory.objects.filter(
            product=self.product
            ).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_quantity + self.quantity
        else:
            totalBal = self.quantity
        # Insert in inventory 
        Inventory.objects.create(
            product = self.product,
            purchase = self,
            sale = None,
            purchase_quantity = self.quantity,
            sale_quantity = None,
            total_balance_quantity = totalBal
        )

class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    customer_mobile = models.CharField(max_length=50)
    customer_address = models.TextField()

    class Meta:
        verbose_name_plural = '7. Customers'

    def __str__(self):
        return self.customer_name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    quantity = models.FloatField()
    price = models.FloatField()
    # It calculates by itself
    total_amount = models.FloatField(editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '5. Sales'
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super(Sale, self).save(*args, **kwargs)

        # Update inventory effect related to sale
        inventory = Inventory.objects.filter(
            product=self.product
            ).order_by('-id').first()
        
        totalBal = 0
        if inventory:
            totalBal = inventory.total_balance_quantity - self.quantity

        # Insert in inventory 
        Inventory.objects.create(
            product = self.product,
            purchase = None,
            sale = self,
            purchase_quantity = None,
            sale_quantity = self.quantity,
            total_balance_quantity = totalBal
        )

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, 
        default=0, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, 
        default=0, null=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    
    purchase_quantity = models.FloatField(default=0, null=True)
    sale_quantity = models.FloatField(default=0, null=True)
    #total_balance_quantity is expressed as, total_balance_quantity = purchase_quantity - sale_quantity
    total_balance_quantity = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = '6. Inventory'
    
    def product_unit(self):
        return self.product.unit.title

    def purchase_date(self):
        if self.purchase:
            return self.purchase.purchase_date

    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
