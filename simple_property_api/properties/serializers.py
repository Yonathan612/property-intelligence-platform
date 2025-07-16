from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'pin',
            'address',
            'business',
            'year',
            'property_class',
            'township_name',
            'zip_code',
            'latitude',
            'longitude',
            'community_area_name'
        ]
    
    def get_address_display(self, obj):
        """Create a display address from available data"""
        if obj.address:
            return obj.address
        # Create address from PIN and community area
        parts = []
        if obj.community_area:
            parts.append(obj.community_area)
        if obj.zip_code:
            parts.append(f"Chicago, IL {obj.zip_code}")
        if parts:
            return " - ".join(parts)
        return f"PIN: {obj.pin}"
    
    def get_pin10(self, obj):
        """Get first 10 characters of PIN"""
        return obj.pin[:10] if obj.pin else ""
    
    def get_coordinates(self, obj):
        """Return coordinates as [lng, lat] array for GeoJSON compatibility"""
        if obj.longitude and obj.latitude:
            return [float(obj.longitude), float(obj.latitude)]
        return None

class PropertyGeoJSONSerializer(serializers.ModelSerializer):
    """Serializer for GeoJSON format"""
    
    def to_representation(self, instance):
        return {
            "type": "Feature",
            "properties": {
                "pin": instance.pin,
                "address": instance.address,
                "zip_code": instance.zip_code,
                "ward": instance.ward,
                "community_area": instance.community_area,
                "property_type": instance.property_type,
                "land_use": instance.land_use,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [instance.longitude, instance.latitude] if instance.longitude and instance.latitude else None
            }
        }
    
    class Meta:
        model = Property
        fields = ['pin', 'address', 'latitude', 'longitude']
