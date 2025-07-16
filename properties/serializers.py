from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

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