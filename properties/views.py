from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Property
from .serializers import PropertySerializer, PropertyGeoJSONSerializer

class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pin'

@api_view(['GET'])
def property_search(request):
    """Search properties by PIN, address, ZIP code, ward, or community area"""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search across multiple fields
    properties = Property.objects.filter(
        Q(pin__icontains=query) |
        Q(address__icontains=query) |
        Q(zip_code__icontains=query) |
        Q(ward__icontains=query) |
        Q(community_area__icontains=query)
    ).distinct()[:20]  # Limit to 20 results
    
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def property_geojson(request):
    """Return all properties in GeoJSON format for map display"""
    properties = Property.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    )[:200]  # Limit for performance
    
    features = []
    for prop in properties:
        serializer = PropertyGeoJSONSerializer(prop)
        features.append(serializer.data)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return Response(geojson)

@api_view(['GET'])
def autocomplete(request):
    """Autocomplete suggestions for search"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return Response([])
    
    # Get suggestions from different fields
    suggestions = []
    
    # PIN suggestions
    pins = Property.objects.filter(pin__icontains=query).values_list('pin', flat=True)[:5]
    for pin in pins:
        suggestions.append({"value": pin, "type": "PIN"})
    
    # Address suggestions
    addresses = Property.objects.filter(address__icontains=query).values_list('address', flat=True)[:5]
    for address in addresses:
        suggestions.append({"value": address, "type": "Address"})
    
    # Community area suggestions
    areas = Property.objects.filter(community_area__icontains=query).values_list('community_area', flat=True).distinct()[:3]
    for area in areas:
        suggestions.append({"value": area, "type": "Community Area"})
    
    return Response(suggestions[:10])  # Limit total suggestions 