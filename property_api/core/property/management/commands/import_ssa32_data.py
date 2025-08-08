import pandas as pd
import traceback
from django.core.management.base import BaseCommand
from core.property.models import Property, PropertySearchIndex


class Command(BaseCommand):
    help = 'Import SSA 32 Properties data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the SSA 32 Properties CSV file')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        clear_data = options['clear']
        
        if clear_data:
            self.stdout.write('Clearing existing property data...')
            Property.objects.all().delete()
            PropertySearchIndex.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        self.stdout.write(f'Reading CSV file: {csv_file}')
        
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            self.stdout.write(f'Found {len(df)} rows in CSV')
            
            # Print column names for debugging
            self.stdout.write(f'CSV columns: {list(df.columns)}')
            
            properties_created = 0
            properties_updated = 0
            
            for index, row in df.iterrows():
                try:
                    property_data = self._convert_row_to_property_data(row)
                    
                    # Try to get existing property by PIN
                    pin = property_data['pin']
                    property_obj, created = Property.objects.get_or_create(
                        pin=pin,
                        defaults=property_data
                    )
                    
                    if created:
                        properties_created += 1
                        if properties_created % 100 == 0:
                            self.stdout.write(f'Created {properties_created} properties...')
                    else:
                        # Update existing property
                        for key, value in property_data.items():
                            setattr(property_obj, key, value)
                        property_obj.save()
                        properties_updated += 1
                        if properties_updated % 100 == 0:
                            self.stdout.write(f'Updated {properties_updated} properties...')
                    
                    # Create or update search index
                    search_text = self._generate_search_text(property_obj)
                    PropertySearchIndex.objects.update_or_create(
                        property=property_obj,
                        defaults={'search_text': search_text}
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing row {index}: {str(e)}')
                    )
                    self.stdout.write(f'Row data: {dict(row)}')
                    traceback.print_exc()
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed! Created: {properties_created}, Updated: {properties_updated}'
                )
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading CSV file: {str(e)}'))
            traceback.print_exc()

    def _convert_row_to_property_data(self, row):
        """Convert a CSV row to Property model data"""
        
        # Clean and normalize data
        pin = self.normalize_pin(row['pin'])
        pin10 = self.generate_pin10(pin)
        
        return {
            # Primary identifiers
            'pin': pin,
            'pin10': pin10,
            'year': int(row['tax_year']) if pd.notna(row['tax_year']) else 2023,
            'class_code': str(row['class']) if pd.notna(row['class']) else '',
            'row_id': self.generate_row_id(row),
            
            # Location data
            'longitude': float(row['longitude']) if pd.notna(row['longitude']) else 0.0,
            'latitude': float(row['latitude']) if pd.notna(row['latitude']) else 0.0,
            'zip_code': self.clean_zip_code(row['property_zip']),
            
            # SSA 32 Property Information
            'property_address': str(row['property_address']) if pd.notna(row['property_address']) else None,
            'property_city': str(row['property_city']) if pd.notna(row['property_city']) else None,
            'property_state': str(row['property_state']) if pd.notna(row['property_state']) else None,
            'square_footage_land': self.clean_square_footage(row['square_footage_land']),
            
            # Assessment Information
            'total_assessed_value': self.clean_currency(row['total_assessed_value']),
            'land_assessed_value': self.clean_currency(row['land_assessed_value']),
            'building_assessed_value': self.clean_currency(row['building_assessed_value']),
            
            # Property Status
            'vacancy_type': str(row['vacancy_type']) if pd.notna(row['vacancy_type']) else None,
            'assessor_office_link': str(row['assessor_office_link']) if pd.notna(row['assessor_office_link']) else None,
            
            # Taxpayer Information
            'taxpayer_id': str(row['taxpayer_id']) if pd.notna(row['taxpayer_id']) else None,
            'mailing_name': str(row['mailing_name']) if pd.notna(row['mailing_name']) else None,
            'mailing_address': str(row['mailing_address']) if pd.notna(row['mailing_address']) else None,
            'mailing_city': str(row['mailing_city']) if pd.notna(row['mailing_city']) else None,
            'mailing_state': str(row['mailing_state']) if pd.notna(row['mailing_state']) else None,
            'mailing_zip': self.clean_zip_code(row['mailing_zip']),
            
            # Administrative divisions (default values for SSA 32)
            'triad_name': 'South',
            'triad_code': 3,
            'township_name': 'South Chicago',
            'township_code': 77,
            'nbhd_code': '72225',  # Default neighborhood code
            'tax_code': str(row['tax_district_code']) if pd.notna(row['tax_district_code']) else '',
            
            # Chicago specific data
            'ward_num': int(row['ward_number']) if pd.notna(row['ward_number']) else None,
        }

    def clean_currency(self, value):
        """Clean currency values and convert to decimal"""
        if pd.isna(value):
            return None
        
        # Convert to string and remove currency symbols and commas
        str_val = str(value).replace('$', '').replace(',', '').strip()
        
        try:
            return float(str_val)
        except (ValueError, TypeError):
            return None

    def clean_square_footage(self, value):
        """Clean square footage values"""
        if pd.isna(value):
            return None
        
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def clean_zip_code(self, value):
        """Clean ZIP code to remove decimal points like '60620.0' -> '60620'"""
        if pd.isna(value):
            return None
        str_val = str(value).strip()
        # Remove decimal point and anything after it
        if '.' in str_val:
            str_val = str_val.split('.')[0]
        return str_val

    def normalize_pin(self, pin_value):
        """Normalize PIN format"""
        if pd.isna(pin_value):
            return ''
        
        pin_str = str(pin_value).strip()
        # Remove any non-numeric characters except hyphens
        pin_str = ''.join(c for c in pin_str if c.isdigit() or c == '-')
        return pin_str

    def generate_pin10(self, pin):
        """Generate 10-digit PIN from full PIN"""
        # Remove hyphens and take first 10 digits
        pin_digits = ''.join(c for c in pin if c.isdigit())
        return pin_digits[:10] if len(pin_digits) >= 10 else pin_digits

    def generate_row_id(self, row):
        """Generate a unique row ID"""
        pin = self.normalize_pin(row['pin'])
        year = int(row['tax_year']) if pd.notna(row['tax_year']) else 2023
        return f"{pin}_{year}"

    def _generate_search_text(self, property_obj):
        """Generate searchable text for the property"""
        search_parts = [
            property_obj.pin,
            property_obj.pin10,
            property_obj.property_address or '',
            property_obj.property_city or '',
            property_obj.property_state or '',
            property_obj.mailing_name or '',
            property_obj.class_code or '',
            property_obj.vacancy_type or '',
            str(property_obj.zip_code or ''),
            str(property_obj.ward_num or ''),
        ]
        
        return ' '.join(filter(None, search_parts)).lower()