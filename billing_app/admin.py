from django.contrib import admin
from .models import Vehicle, SparePart, Customer, Invoice, InvoiceItem

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'battery_type', 'range_km', 'price')
    search_fields = ('name',)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'applicable_models')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'aadhar_no')
    search_fields = ('name', 'mobile', 'aadhar_no')

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('unique_bill_id', 'customer', 'subtotal', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('unique_bill_id', 'customer__name', 'customer__mobile')
    readonly_fields = ('unique_bill_id', 'cgst', 'sgst', 'total_amount', 'created_at')
    inlines = [InvoiceItemInline]
