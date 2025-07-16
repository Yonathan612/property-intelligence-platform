from django.urls import path
from . import views

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property-list'),
    path('search/', views.property_search, name='property-search'),
    path('geojson/', views.property_geojson, name='property-geojson'),
    path('autocomplete/', views.autocomplete, name='property-autocomplete'),
    path('<str:pin>/', views.PropertyDetailView.as_view(), name='property-detail'),
] 