import pandas as pd
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.property.models import Property, PropertySearchIndex


class Command(BaseCommand):
    help = 'Import property data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            type=str,
            help='Path to the CSV file (default: data/common_county_data_complete.csv)',
            default='data/common_county_data_complete.csv'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of records to process in each batch'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        batch_size = options['batch_size']
        clear_data = options['clear']

        # Resolve CSV path relative to project root
        if not os.path.isabs(csv_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            csv_path = os.path.join(project_root, '..', csv_path)

        if not os.path.exists(csv_path):
            raise CommandError(f'CSV file not found: {csv_path}')

        self.stdout.write(f'Loading CSV data from: {csv_path}')

        # Clear existing data if requested
        if clear_data:
            self.stdout.write('Clearing existing property data...')
            Property.objects.all().delete()
            PropertySearchIndex.objects.all().delete()

        try:
            # Read CSV file
            self.stdout.write('Reading CSV file...')
            df = pd.read_csv(csv_path)
            total_rows = len(df)
            self.stdout.write(f'Found {total_rows} records in CSV file')

            # Process data in batches
            created_count = 0
            error_count = 0

            for i in range(0, total_rows, batch_size):
                batch_df = df.iloc[i:i+batch_size]
                batch_properties = []

                for _, row in batch_df.iterrows():
                    try:
                        # Convert pandas types to Python types and handle NaN
                        property_data = self._convert_row_to_property_data(row)
                        property_obj = Property(**property_data)
                        batch_properties.append(property_obj)
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'Error processing row {i}: {str(e)}')
                        )

                # Bulk create properties
                if batch_properties:
                    try:
                        Property.objects.bulk_create(batch_properties, ignore_conflicts=True)
                        created_count += len(batch_properties)
                        self.stdout.write(f'Processed batch {i//batch_size + 1}: {len(batch_properties)} records')
                    except Exception as e:
                        error_count += len(batch_properties)
                        self.stdout.write(
                            self.style.ERROR(f'Error creating batch: {str(e)}')
                        )

            # Create search indices
            self.stdout.write('Creating search indices...')
            self._create_search_indices()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed! Created: {created_count}, Errors: {error_count}'
                )
            )

        except Exception as e:
            raise CommandError(f'Error processing CSV file: {str(e)}')

    def _convert_row_to_property_data(self, row):
        """Convert pandas row to Property model data, handling NaN values"""
        
        def safe_float(value):
            return None if pd.isna(value) else float(value)
        
        def safe_int(value):
            return None if pd.isna(value) else int(value)
        
        def safe_str(value):
            return None if pd.isna(value) else str(value)
        
        def safe_bool(value):
            if pd.isna(value):
                return None
            return bool(value) if isinstance(value, bool) else str(value).lower() in ['true', '1', 'yes']

        return {
            'pin': safe_str(row['pin']),
            'pin10': safe_str(row['pin10']),
            'year': safe_int(row['year']),
            'class_code': safe_str(row['class']),
            'row_id': safe_str(row['row_id']),
            'longitude': safe_float(row['lon']),
            'latitude': safe_float(row['lat']),
            'x_3435': safe_float(row['x_3435']),
            'y_3435': safe_float(row['y_3435']),
            'zip_code': safe_str(row['zip_code']),
            'triad_name': safe_str(row['triad_name']),
            'triad_code': safe_int(row['triad_code']),
            'township_name': safe_str(row['township_name']),
            'township_code': safe_int(row['township_code']),
            'nbhd_code': safe_str(row['nbhd_code']),
            'tax_code': safe_str(row['tax_code']),
            'census_block_group_geoid': safe_str(row['census_block_group_geoid']),
            'census_block_geoid': safe_str(row['census_block_geoid']),
            'census_congressional_district_geoid': safe_str(row['census_congressional_district_geoid']),
            'census_congressional_district_num': safe_int(row['census_congressional_district_num']),
            'census_tract_geoid': safe_str(row['census_tract_geoid']),
            'census_data_year': safe_int(row['census_data_year']),
            'ward_num': safe_int(row['ward_num']),
            'ward_chicago_data_year': safe_int(row['ward_chicago_data_year']),
            'chicago_community_area_num': safe_int(row['chicago_community_area_num']),
            'chicago_community_area_name': safe_str(row['chicago_community_area_name']),
            'chicago_police_district_num': safe_int(row['chicago_police_district_num']),
            'school_elementary_district_geoid': safe_str(row['school_elementary_district_geoid']),
            'school_elementary_district_name': safe_str(row['school_elementary_district_name']),
            'school_secondary_district_geoid': safe_str(row['school_secondary_district_geoid']),
            'school_secondary_district_name': safe_str(row['school_secondary_district_name']),
            'school_unified_district_geoid': safe_str(row['school_unified_district_geoid']),
            'school_unified_district_name': safe_str(row['school_unified_district_name']),
            'school_school_year': safe_str(row['school_school_year']),
            'school_data_year': safe_int(row['school_data_year']),
            'tax_municipality_num': safe_str(row['tax_municipality_num']),
            'tax_municipality_name': safe_str(row['tax_municipality_name']),
            'tax_school_elementary_district_num': safe_str(row['tax_school_elementary_district_num']),
            'tax_school_elementary_district_name': safe_str(row['tax_school_elementary_district_name']),
            'tax_school_secondary_district_num': safe_str(row['tax_school_secondary_district_num']),
            'tax_school_secondary_district_name': safe_str(row['tax_school_secondary_district_name']),
            'tax_community_college_district_num': safe_str(row['tax_community_college_district_num']),
            'tax_community_college_district_name': safe_str(row['tax_community_college_district_name']),
            'tax_fire_protection_district_num': safe_str(row['tax_fire_protection_district_num']),
            'tax_fire_protection_district_name': safe_str(row['tax_fire_protection_district_name']),
            'tax_library_district_num': safe_str(row['tax_library_district_num']),
            'tax_library_district_name': safe_str(row['tax_library_district_name']),
            'tax_park_district_num': safe_str(row['tax_park_district_num']),
            'tax_park_district_name': safe_str(row['tax_park_district_name']),
            'tax_tif_district_num': safe_float(row['tax_tif_district_num']),
            'tax_tif_district_name': safe_str(row['tax_tif_district_name']),
            'tax_data_year': safe_int(row['tax_data_year']),
            'env_flood_fema_sfha': safe_bool(row['env_flood_fema_sfha']),
            'env_flood_fema_data_year': safe_int(row['env_flood_fema_data_year']),
            'env_flood_fs_factor': safe_float(row['env_flood_fs_factor']),
            'env_flood_fs_risk_direction': safe_str(row['env_flood_fs_risk_direction']),
            'env_ohare_noise_contour_no_buffer_bool': safe_bool(row['env_ohare_noise_contour_no_buffer_bool']),
            'env_ohare_noise_contour_half_mile_buffer_bool': safe_bool(row['env_ohare_noise_contour_half_mile_buffer_bool']),
            'env_airport_noise_dnl': safe_float(row['env_airport_noise_dnl']),
            'econ_enterprise_zone_num': safe_str(row['econ_enterprise_zone_num']),
            'econ_qualified_opportunity_zone_num': safe_str(row['econ_qualified_opportunity_zone_num']),
            'access_cmap_walk_id': safe_int(row['access_cmap_walk_id']),
            'access_cmap_walk_nta_score': safe_float(row['access_cmap_walk_nta_score']),
            'access_cmap_walk_total_score': safe_float(row['access_cmap_walk_total_score']),
            'access_cmap_walk_data_year': safe_int(row['access_cmap_walk_data_year']),
            'misc_subdivision_id': safe_str(row['misc_subdivision_id']),
            'misc_subdivision_data_year': safe_float(row['misc_subdivision_data_year']),
        }

    def _create_search_indices(self):
        """Create search indices for existing properties"""
        properties = Property.objects.all()
        search_indices = []

        for prop in properties:
            search_text_parts = []
            
            # Add searchable fields
            if prop.pin:
                search_text_parts.append(prop.pin)
            if prop.pin10:
                search_text_parts.append(prop.pin10)
            if prop.chicago_community_area_name:
                search_text_parts.append(prop.chicago_community_area_name)
            if prop.zip_code:
                search_text_parts.append(prop.zip_code)
            if prop.township_name:
                search_text_parts.append(prop.township_name)
            if prop.tax_municipality_name:
                search_text_parts.append(prop.tax_municipality_name)

            search_text = ' '.join(search_text_parts)
            
            search_index = PropertySearchIndex(
                property=prop,
                search_text=search_text
            )
            search_indices.append(search_index)

        # Bulk create search indices
        PropertySearchIndex.objects.bulk_create(search_indices, ignore_conflicts=True)
        self.stdout.write(f'Created {len(search_indices)} search indices') 