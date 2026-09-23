import io
import os
import json
import base64
import qrcode
import pandas as pd
from django.conf import settings
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from .models import Invoice, Customer, Vehicle, SparePart, InvoiceItem
from .forms import CustomerForm, InvoiceForm

@login_required(login_url='/admin/login/?next=/create-invoice/')
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            cust_data = data.get('customer', {})
            mobile = cust_data.get('mobile', '').strip()
            name = cust_data.get('name', '').strip()
            address = cust_data.get('address', '').strip()
            aadhar_no = cust_data.get('aadhar_no', '').strip()

            if not mobile or not name or not address:
                return JsonResponse({'status': 'error', 'message': 'Customer Name, Mobile, and Address are required.'}, status=400)

            items_data = data.get('items', [])
            if not items_data:
                return JsonResponse({'status': 'error', 'message': 'Please add at least one item to the invoice.'}, status=400)

            # 1. Create or Get Customer safely (matching by mobile without MultipleObjectsReturned)
            mobile_digits = ''.join(ch for ch in mobile if ch.isdigit())
            ten_digit_mobile = mobile_digits[-10:] if len(mobile_digits) >= 10 else mobile

            customer = Customer.objects.filter(
                Q(mobile=mobile) | Q(mobile=ten_digit_mobile) | Q(mobile='0' + ten_digit_mobile)
            ).first()

            if customer:
                customer.name = name
                customer.address = address
                if aadhar_no:
                    customer.aadhar_no = aadhar_no
                customer.save()
            else:
                customer = Customer.objects.create(
                    mobile=mobile,
                    name=name,
                    address=address,
                    aadhar_no=aadhar_no or None,
                )
            
            # 2. Create Invoice & Items atomically
            with transaction.atomic():
                invoice = Invoice.objects.create(customer=customer)
                subtotal = 0.0
                for item in items_data:
                    qty = int(item.get('quantity', 1))
                    rate = float(item.get('rate', 0.0))
                    amount = round(rate * qty, 2)
                    subtotal += amount
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        item_name=item.get('name', '').strip(),
                        hardware_details=item.get('hardware', '').strip() or None,
                        hsn_code=item.get('hsn', '8714').strip() or '8714',
                        quantity=qty,
                        rate=rate,
                        amount=amount
                    )
                
                invoice.subtotal = round(subtotal, 2)
                invoice.save() # Triggers model's auto-calculation for GST and Total
            
            return JsonResponse({'status': 'success', 'redirect_url': f'/invoice/{invoice.unique_bill_id}/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        vehicles = Vehicle.objects.all()
        spares = SparePart.objects.all()
        customer_form = CustomerForm()
        return render(request, 'billing_app/create_invoice.html', {
            'vehicles': vehicles,
            'spares': spares,
            'customer_form': customer_form,
        })

def view_invoice_pdf(request, unique_bill_id):
    invoice = get_object_or_404(Invoice, unique_bill_id=unique_bill_id)

    # Generate QR Code linking to absolute URI
    uri = request.build_absolute_uri()
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Load Logo base64 for reliable xhtml2pdf embedding
    logo_base64 = ""
    logo_path = os.path.join(settings.BASE_DIR, 'billing_app', 'static', 'billing_app', 'images', 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_base64 = base64.b64encode(f.read()).decode('utf-8')

    def wrap_serial(val):
        if not val:
            return ""
        # Insert space every 12 characters so xhtml2pdf can wrap long unbroken serials gracefully
        words = val.split()
        wrapped_words = []
        for word in words:
            if len(word) > 12:
                wrapped_words.append(" ".join(word[i:i+12] for i in range(0, len(word), 12)))
            else:
                wrapped_words.append(word)
        return " ".join(wrapped_words)

    # Prepare items with safely wrapped hardware details for clean PDF rendering
    pdf_items = []
    for item in invoice.items.all():
        pdf_items.append({
            'item_name': item.item_name,
            'hardware_details': wrap_serial(item.hardware_details) if item.hardware_details else '',
            'hsn_code': item.hsn_code or '8714',
            'quantity': item.quantity,
            'rate': item.rate,
            'amount': item.amount,
        })

    context = {
        'invoice': invoice,
        'items': pdf_items,
        'qr_base64': qr_base64,
        'logo_base64': logo_base64,
    }

    html_string = render_to_string('billing_app/invoice_pdf.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{invoice.unique_bill_id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors drawing the PDF')
    return response

def home(request):
    # --- AUTO-CREATE SUPERUSER SNIPPET (Temporary) ---
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Admin@12345')
            print("Superuser 'admin' created successfully!")
    except Exception as e:
        print("Error creating superuser:", e)
    # ---------------------------------------------------

    vehicles = Vehicle.objects.all()[:6]
    return render(request, 'billing_app/home.html', {'vehicles': vehicles})

def catalog(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'billing_app/catalog.html', {'vehicles': vehicles})

# --- TEMPORARY IMPORT VIEW ---
def trigger_import(request):
    # Security check: Sirf logged in admin hi is link ko run kar sake
    if not request.user.is_superuser:
        return HttpResponse("Aap admin nahi ho, isliye access denied!", status=401)
        
    dealer_file = os.path.join(settings.BASE_DIR, 'KOMAKI DEALER RATE LIST (1)-2.xlsx')
    spare_file = os.path.join(settings.BASE_DIR, 'spare parts.xls')
    
    output = []
    
    # 1. IMPORT VEHICLES
    if os.path.exists(dealer_file):
        try:
            df_vehicles = pd.read_excel(dealer_file, sheet_name='SATYAM MOTORS', header=2)
            count = 0
            for index, row in df_vehicles.iterrows():
                model_name = str(row.get('MODEL ', '')).strip()
                if model_name and model_name.lower() != 'nan':
                    raw_price = str(row.get('SALE RATE AS PER CITY', row.get('DEALER RATE', 0.0)))
                    clean_price = raw_price.replace(',', '').strip()
                    try:
                        price = float(clean_price)
                    except ValueError:
                        price = 0.0

                    battery = str(row.get('BATTERY TYPE', '')).strip()
                    range_km = str(row.get('RANGE (DISTANCE)', '')).strip()

                    Vehicle.objects.get_or_create(
                        name=model_name,
                        defaults={'price': price, 'battery_type': battery, 'range_km': range_km}
                    )
                    count += 1
            output.append(f"✅ {count} Vehicles imported successfully!")
        except Exception as e:
            output.append(f"❌ Error importing Vehicles: {e}")
    else:
        output.append(f"File not found: {dealer_file}")

    # 2. IMPORT SPARES
    if os.path.exists(spare_file):
        try:
            df_spares = pd.read_excel(spare_file, sheet_name='XGT KM', header=2)
            count = 0
            for index, row in df_spares.iterrows():
                item_name = str(row.get('ITEMS ', '')).strip()
                if item_name and item_name.lower() != 'nan':
                    base_price = row.get('X1/KM', None)
                    if pd.isna(base_price):
                        base_price = row.get('SE/X4', 0.0)
                    
                    raw_sp_price = str(base_price).replace(',', '').strip()
                    try:
                        price = float(raw_sp_price)
                    except ValueError:
                        price = 0.0

                    SparePart.objects.get_or_create(
                        name=f"{item_name} (Standard)",
                        defaults={'price': price}
                    )
                    count += 1
            output.append(f"✅ {count} Spare Parts imported successfully!")
        except Exception as e:
            output.append(f"❌ Error importing Spare Parts: {e}")
    else:
        output.append(f"File not found: {spare_file}")

    return HttpResponse("<br>".join(output))