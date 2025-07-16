import csv
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_api.settings')
django.setup()

from properties.models import Property

def load_properties():
    # Clear existing data
    Property.objects.all().delete()
    
    # Read CSV file
    csv_file = '../data/79thProperties.csv'
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        properties = []
        
        for row in csv_reader:
            try:
                property = Property(
                    pin=row['pins'],
                    address=row['Address'],
                    business=row['Business'],
                    year=int(row['year']),
                    property_class=row['class'],
                    township_name=row['township_name'],
                    zip_code=str(float(row['zip_code'])).split('.')[0],  # Remove decimal
                    latitude=float(row['lat']),
                    longitude=float(row['lon']),
                    community_area_name=row['chicago_community_area_name']
                )
                properties.append(property)
            except Exception as e:
                print(f"Error processing row: {row['pins']}")
                print(f"Error: {str(e)}")
                continue
        
        # Bulk create properties
        Property.objects.bulk_create(properties)
        print(f"Successfully imported {len(properties)} properties")

if __name__ == '__main__':
    load_properties()
