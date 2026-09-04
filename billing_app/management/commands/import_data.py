import pandas as pd
from django.core.management.base import BaseCommand
from billing_app.models import Vehicle, SparePart

class Command(BaseCommand):
    help = 'Imports vehicles and spare parts data from Excel files'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')
        
        # 1. Import Vehicles
        vehicles_file = 'KOMAKI DEALER RATE LIST (1)-2.xlsx'
        try:
            # skiprows=2 means skip first two rows (0 and 1)
            df_vehicles = pd.read_excel(vehicles_file, skiprows=2)
            
            for index, row in df_vehicles.iterrows():
                model_name = str(row.get('MODEL ')).strip() if pd.notna(row.get('MODEL ')) else None
                battery = str(row.get('BATTERY TYPE')).strip() if pd.notna(row.get('BATTERY TYPE')) else ''
                range_dist = str(row.get('RANGE (DISTANCE)')).strip() if pd.notna(row.get('RANGE (DISTANCE)')) else ''
                price_val = row.get('SALE RATE AS PER CITY')
                
                if pd.isna(price_val):
                    price_val = 0.0
                else:
                    # Remove commas and convert to float
                    price_val = str(price_val).replace(',', '')
                
                if model_name and model_name.lower() != 'nan':
                    Vehicle.objects.update_or_create(
                        name=model_name,
                        defaults={
                            'battery_type': battery,
                            'range_km': range_dist,
                            'price': float(price_val)
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported vehicles.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing vehicles: {e}'))

        # 2. Import Spare Parts
        spare_parts_file = 'spare parts.xls'
        try:
            df_spares = pd.read_excel(spare_parts_file, sheet_name='XGT KM', skiprows=2)
            
            for index, row in df_spares.iterrows():
                item_name = str(row.get('ITEMS ')).strip() if pd.notna(row.get('ITEMS ')) else None
                
                # Calculate max price from available columns
                prices = []
                for col in ['X1/KM', 'SE/X4', 'X3', 'MG PRO', 'XR7']:
                    val = row.get(col)
                    # Convert to float safely, handling strings like '100.5' or '-'
                    if pd.notna(val):
                        try:
                            prices.append(float(val))
                        except ValueError:
                            pass
                
                max_price = max(prices) if prices else 0.0
                
                if item_name and item_name.lower() != 'nan':
                    SparePart.objects.update_or_create(
                        name=item_name,
                        defaults={
                            'price': max_price,
                            'applicable_models': 'XGT KM (Imported)'
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported spare parts.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing spare parts: {e}'))
