import os
import django
import pandas as pd

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'np_motors_project.settings')
django.setup()

from billing_app.models import Vehicle, SparePart

def import_data():
    dealer_file = 'KOMAKI DEALER RATE LIST (1)-2.xlsx'
    spare_file = 'spare parts.xls'

    # 1. IMPORT VEHICLES
    print(f"Reading Vehicles from: {dealer_file}")
    if os.path.exists(dealer_file):
        try:
            df_vehicles = pd.read_excel(dealer_file, sheet_name='SATYAM MOTORS', header=2)
            
            for index, row in df_vehicles.iterrows():
                model_name = str(row.get('MODEL ', '')).strip()
                if model_name and model_name.lower() != 'nan':
                    # Extract price, convert to string, remove commas, then convert to float
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
                        defaults={
                            'price': price,
                            'battery_type': battery,
                            'range_km': range_km,
                        }
                    )
            print("✅ Vehicles imported successfully!")
        except Exception as e:
            print(f"❌ Error importing Vehicles: {e}")
    else:
        print(f"File not found: {dealer_file}")

    # 2. IMPORT SPARE PARTS
    print(f"\nReading Spare Parts from: {spare_file}")
    if os.path.exists(spare_file):
        try:
            df_spares = pd.read_excel(spare_file, sheet_name='XGT KM', header=2)
            
            for index, row in df_spares.iterrows():
                item_name = str(row.get('ITEMS ', '')).strip()
                if item_name and item_name.lower() != 'nan':
                    base_price = row.get('X1/KM', None)
                    if pd.isna(base_price):
                        base_price = row.get('SE/X4', 0.0)
                    
                    # Remove commas here too, just to be safe
                    raw_sp_price = str(base_price).replace(',', '').strip()
                    try:
                        price = float(raw_sp_price)
                    except ValueError:
                        price = 0.0

                    SparePart.objects.get_or_create(
                        name=f"{item_name} (Standard)",
                        defaults={'price': price}
                    )
            print("✅ Spare Parts imported successfully!")
        except Exception as e:
            print(f"❌ Error importing Spare Parts: {e}")
    else:
        print(f"File not found: {spare_file}")

if __name__ == '__main__':
    import_data()