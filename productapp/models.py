from django.db import models
from django.db import models
from django.utils import timezone
from uuid import uuid4

# Create your models here.

class Invoice(models.Model):
    method = [
        ('Bank Transfer', 'Bank Transfer'),
        ('POS', 'POS'),
        ('Cash', 'Cash'),
    ]

    status = [
        ('Pending', 'Pending'),
        ('Credit', 'Credit'),
        ('Paid', 'Paid'),
    ]


    invoice_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=50, null=True, blank=True, unique=False)
    client_phone = models.CharField(max_length=50, null=True, blank=True, unique=False)
    number = models.CharField(null=True, blank=True, max_length=100)
    payment_method = models.CharField(choices=method, null=True, blank=True, max_length=50)
    payment_status = models.CharField(choices=status, null=False, default='Pending', max_length=50)
    agent = models.CharField(max_length=50, blank=True, null=True)
    

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f'INV0{self.invoice_id}-{self.client_name}'
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            
        self.last_updated = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)
    

class Product(models.Model):
    unit = [
        ('Pack(s)', 'Pack(s)'),
        ('Piece(s)', 'Piece(s)'),
        ('Kg','Kg')
    ]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, null=False, blank=False, unique=False)
    price_per_Qty = models.FloatField(unique=False, blank=False, null=False)
    total_price = models.FloatField(unique=False, blank=False, null=False, default = 0.0)
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.CharField(choices=unit, null=False, default='Piece(s)', max_length=50)
    invoice = models.ForeignKey(Invoice, blank=True, null=True,  on_delete=models.CASCADE)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)



    def __str__(self):
        return f'PRD0{self.product_id}-{self.product_name}'
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            
        self.last_updated = timezone.localtime(timezone.now())

        super(Product, self).save(*args, **kwargs)
