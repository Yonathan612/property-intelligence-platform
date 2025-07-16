from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pin'

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        search_type = request.query_params.get('type', 'all')
        limit = int(request.query_params.get('limit', 50))

        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Build search query
        if search_type == 'pin':
            queryset = Property.objects.filter(pin__startswith=query)
        elif search_type == 'address':
            queryset = Property.objects.filter(address__icontains=query)
        elif search_type == 'business':
            queryset = Property.objects.filter(business__icontains=query)
        else:  # 'all'
            queryset = Property.objects.filter(
                Q(pin__startswith=query) |
                Q(address__icontains=query) |
                Q(business__icontains=query)
            )

        # Limit results
        queryset = queryset[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        query = request.query_params.get('q', '')
        limit = int(request.query_params.get('limit', 10))

        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Search across PIN, address, and business name
        queryset = Property.objects.filter(
            Q(pin__startswith=query) |
            Q(address__icontains=query) |
            Q(business__icontains=query)
        )[:limit]

        # Return simplified results for autocomplete
        results = [
            {
                'pin': prop.pin,
                'display': f"{prop.address} - {prop.business}" if prop.business else prop.address
            }
            for prop in queryset
        ]
        return Response(results)
