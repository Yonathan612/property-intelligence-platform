from django.db.models import Q, Count
from django.db import models
from django.http import JsonResponse
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Property
from .serializers import (
    PropertySummarySerializer, PropertyDetailSerializer,
    PropertyLocationSerializer, PropertySchoolInfoSerializer,
    PropertyTaxInfoSerializer, PropertyEnvironmentalSerializer,
    PropertyGeoJSONSerializer
)


class PropertyPagination(PageNumberPagination):
    """Custom pagination for property listings"""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class PropertyListView(generics.ListAPIView):
    """
    List all properties with optional filtering
    """
    queryset = Property.objects.all()
    serializer_class = PropertySummarySerializer
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = [
        'class_code', 'zip_code', 'ward_num', 'township_name',
        'chicago_community_area_name', 'triad_name'
    ]
    search_fields = [
        'pin', 'pin10', 'chicago_community_area_name', 'zip_code'
    ]
    ordering_fields = ['pin', 'zip_code', 'ward_num']
    ordering = ['pin']


class PropertyDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed information for a specific property by PIN
    """
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    lookup_field = 'pin'


@api_view(['GET'])
def property_search(request):
    """
    Advanced search endpoint for properties
    Supports search by PIN, partial PIN, ZIP code, community area
    """
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'all')  # all, pin, zip, area
    limit = min(int(request.GET.get('limit', 50)), 100)
    
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Build search filters based on type
    if search_type == 'pin':
        queryset = Property.objects.filter(
            Q(pin__icontains=query) | Q(pin10__icontains=query)
        )
    elif search_type == 'zip':
        queryset = Property.objects.filter(zip_code__icontains=query)
    elif search_type == 'area':
        queryset = Property.objects.filter(
            chicago_community_area_name__icontains=query
        )
    else:  # search_type == 'all'
        queryset = Property.objects.filter(
            Q(pin__icontains=query) |
            Q(pin10__icontains=query) |
            Q(zip_code__icontains=query) |
            Q(chicago_community_area_name__icontains=query) |
            Q(township_name__icontains=query)
        )
    
    # Limit results and serialize
    properties = queryset[:limit]
    serializer = PropertySummarySerializer(properties, many=True)
    
    return Response({
        'count': queryset.count(),
        'results': serializer.data,
        'query': query,
        'search_type': search_type
    })


@api_view(['GET'])
def property_nearby(request):
    """
    Find properties near a given location
    """
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        radius = float(request.GET.get('radius', 1.0))  # km
        limit = min(int(request.GET.get('limit', 25)), 100)
    except (TypeError, ValueError):
        return Response({'error': 'Invalid lat, lon, or radius parameters'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Simple bounding box search
    lat_delta = radius / 111.0
    lon_delta = radius / (111.0 * abs(lat))
    
    properties = Property.objects.filter(
        latitude__range=(lat - lat_delta, lat + lat_delta),
        longitude__range=(lon - lon_delta, lon + lon_delta)
    )[:limit]
    
    serializer = PropertyLocationSerializer(properties, many=True)
    return Response({
        'count': properties.count(),
        'center': [lon, lat],
        'radius_km': radius,
        'results': serializer.data
    })


@api_view(['GET'])
def property_geojson(request):
    """
    Return properties as GeoJSON for map visualization
    """
    # Apply filters
    queryset = Property.objects.all()
    
    # Filter by bounding box if provided
    if all(param in request.GET for param in ['north', 'south', 'east', 'west']):
        try:
            north = float(request.GET['north'])
            south = float(request.GET['south'])
            east = float(request.GET['east'])
            west = float(request.GET['west'])
            
            queryset = queryset.filter(
                latitude__range=(south, north),
                longitude__range=(west, east)
            )
        except ValueError:
            pass
    
    # Filter by community area
    if 'area' in request.GET:
        queryset = queryset.filter(
            chicago_community_area_name__icontains=request.GET['area']
        )
    
    # Filter by class code
    if 'class' in request.GET:
        queryset = queryset.filter(class_code=request.GET['class'])
    
    # Limit results for performance
    limit = min(int(request.GET.get('limit', 500)), 1000)
    properties = queryset[:limit]
    
    # Create GeoJSON FeatureCollection
    features = []
    for prop in properties:
        serializer = PropertyGeoJSONSerializer(prop)
        features.append(serializer.data)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return JsonResponse(geojson)


class PropertySchoolInfoView(generics.RetrieveAPIView):
    """
    Get school district information for a property
    """
    queryset = Property.objects.all()
    serializer_class = PropertySchoolInfoSerializer
    lookup_field = 'pin'


class PropertyTaxInfoView(generics.RetrieveAPIView):
    """
    Get tax district information for a property
    """
    queryset = Property.objects.all()
    serializer_class = PropertyTaxInfoSerializer
    lookup_field = 'pin'


class PropertyEnvironmentalView(generics.RetrieveAPIView):
    """
    Get environmental information for a property
    """
    queryset = Property.objects.all()
    serializer_class = PropertyEnvironmentalSerializer
    lookup_field = 'pin'


@api_view(['GET'])
def property_statistics(request):
    """
    Get summary statistics about the property database
    """
    stats = {
        'total_properties': Property.objects.count(),
        'community_areas': Property.objects.values('chicago_community_area_name')
                                          .distinct().count(),
        'zip_codes': Property.objects.values('zip_code').distinct().count(),
        'wards': Property.objects.values('ward_num').distinct().count(),
        'property_classes': Property.objects.values('class_code').distinct().count(),
    }
    
    # Top community areas by property count
    top_areas = Property.objects.values('chicago_community_area_name') \
                               .annotate(count=models.Count('id')) \
                               .order_by('-count')[:10]
    
    stats['top_community_areas'] = list(top_areas)
    
    return Response(stats)


@api_view(['GET'])
def autocomplete_search(request):
    """
    Autocomplete suggestions for search queries
    """
    query = request.GET.get('q', '').strip()
    limit = min(int(request.GET.get('limit', 10)), 20)
    
    if len(query) < 2:
        return Response({'suggestions': []})
    
    suggestions = []
    
    # PIN suggestions
    pins = Property.objects.filter(pin__startswith=query) \
                          .values_list('pin', flat=True)[:limit//2]
    suggestions.extend([{'value': pin, 'type': 'pin'} for pin in pins])
    
    # Community area suggestions
    areas = Property.objects.filter(
        chicago_community_area_name__icontains=query
    ).values_list('chicago_community_area_name', flat=True) \
     .distinct()[:limit//2]
    
    suggestions.extend([{'value': area, 'type': 'area'} for area in areas if area])
    
    return Response({'suggestions': suggestions[:limit]}) 