from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    # Property list and detail views
    path('', views.PropertyListView.as_view(), name='property-list'),
    path('<str:pin>/', views.PropertyDetailView.as_view(), name='property-detail'),
    
    # Search endpoints
    path('search/', views.property_search, name='property-search'),
    path('autocomplete/', views.autocomplete_search, name='autocomplete-search'),
    path('nearby/', views.property_nearby, name='property-nearby'),
    
    # Specialized information endpoints
    path('<str:pin>/schools/', views.PropertySchoolInfoView.as_view(), name='property-schools'),
    path('<str:pin>/tax/', views.PropertyTaxInfoView.as_view(), name='property-tax'),
    path('<str:pin>/environment/', views.PropertyEnvironmentalView.as_view(), name='property-environment'),
    
    # Map data endpoints
    path('geojson/', views.property_geojson, name='property-geojson'),
    
    # Statistics endpoint
    path('stats/', views.property_statistics, name='property-statistics'),
] 