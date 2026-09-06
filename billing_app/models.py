import uuid
from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    battery_type = models.CharField(max_length=100)
    range_km = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/', null=True, blank=True)

    def __str__(self):
        return self.name

class SparePart(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_models = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    aadhar_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.mobile})"

class Invoice(models.Model):
    unique_bill_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.subtotal:
            self.cgst = round(float(self.subtotal) * 0.025, 2)
            self.sgst = round(float(self.subtotal) * 0.025, 2)
            self.total_amount = float(self.subtotal) + float(self.cgst) + float(self.sgst)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.unique_bill_id} - {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    hardware_details = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} (x{self.quantity})"
