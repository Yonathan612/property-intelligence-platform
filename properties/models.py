from django.db import models

class Property(models.Model):
    # Basic property information
    pin = models.CharField(max_length=20, unique=True, db_index=True)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, blank=True, db_index=True)
    
    # Location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Administrative divisions
    ward = models.CharField(max_length=10, blank=True, db_index=True)
    community_area = models.CharField(max_length=100, blank=True, db_index=True)
    community_area_number = models.IntegerField(null=True, blank=True)
    
    # Property details
    property_type = models.CharField(max_length=50, blank=True)
    land_use = models.CharField(max_length=100, blank=True)
    building_class = models.CharField(max_length=10, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['pin']
    
    def __str__(self):
        return f"{self.pin} - {self.address}" 