from rest_framework import serializers
from .models import Property, PropertySearchIndex


class PropertySummarySerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for property list views and map markers
    """
    coordinates = serializers.ReadOnlyField()
    address_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'pin', 'pin10', 'coordinates', 'address_display',
            'chicago_community_area_name', 'zip_code', 'ward_num',
            'township_name', 'class_code', 'property_address',
            'property_city', 'property_state', 'total_assessed_value',
            'vacancy_type', 'mailing_name', 'year', 'square_footage_land',
            'land_assessed_value', 'building_assessed_value', 'taxpayer_id',
            'mailing_address', 'mailing_city', 'mailing_state', 'mailing_zip',
            'tax_code', 'assessor_office_link'
        ]


class PropertyDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for detailed property information
    """
    coordinates = serializers.ReadOnlyField()
    address_display = serializers.ReadOnlyField()
    nearby_properties_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = '__all__'
    
    def get_nearby_properties_count(self, obj):
        """Return count of nearby properties within 1km"""
        return obj.nearby_properties().count()


class PropertyLocationSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for location-based queries
    """
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'pin', 'coordinates', 'chicago_community_area_name',
            'zip_code', 'address_display'
        ]


class PropertySchoolInfoSerializer(serializers.ModelSerializer):
    """
    Serializer focused on school district information
    """
    coordinates = serializers.ReadOnlyField()
    address_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'pin', 'coordinates', 'address_display',
            'school_elementary_district_name',
            'school_secondary_district_name', 
            'school_unified_district_name',
            'school_school_year', 'school_data_year'
        ]


class PropertyTaxInfoSerializer(serializers.ModelSerializer):
    """
    Serializer focused on tax district information
    """
    coordinates = serializers.ReadOnlyField()
    address_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'pin', 'coordinates', 'address_display',
            'tax_municipality_name',
            'tax_school_elementary_district_name',
            'tax_school_secondary_district_name',
            'tax_community_college_district_name',
            'tax_fire_protection_district_name',
            'tax_library_district_name',
            'tax_park_district_name',
            'tax_tif_district_name',
            'tax_data_year'
        ]


class PropertyEnvironmentalSerializer(serializers.ModelSerializer):
    """
    Serializer focused on environmental information
    """
    coordinates = serializers.ReadOnlyField()
    address_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'pin', 'coordinates', 'address_display',
            'env_flood_fema_sfha',
            'env_flood_fs_factor',
            'env_flood_fs_risk_direction',
            'env_ohare_noise_contour_no_buffer_bool',
            'env_ohare_noise_contour_half_mile_buffer_bool',
            'env_airport_noise_dnl',
            'econ_enterprise_zone_num',
            'econ_qualified_opportunity_zone_num'
        ]


class PropertyGeoJSONSerializer(serializers.ModelSerializer):
    """
    GeoJSON-compatible serializer for map visualization
    """
    
    class Meta:
        model = Property
        fields = [
            'pin', 'longitude', 'latitude', 'chicago_community_area_name',
            'zip_code', 'class_code', 'ward_num'
        ]
    
    def to_representation(self, instance):
        """Convert to GeoJSON feature format"""
        data = super().to_representation(instance)
        
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [instance.longitude, instance.latitude]
            },
            "properties": {
                "pin": data['pin'],
                "community_area": data['chicago_community_area_name'],
                "zip_code": data['zip_code'],
                "class_code": data['class_code'],
                "ward": data['ward_num'],
                "popup_content": f"PIN: {data['pin']}<br/>Area: {data['chicago_community_area_name'] or 'Unknown'}<br/>ZIP: {data['zip_code'] or 'N/A'}"
            }
        } 