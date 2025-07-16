from django.db import models

class Property(models.Model):
    pin = models.CharField(max_length=14, primary_key=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    business = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    property_class = models.CharField(max_length=10, null=True, blank=True)
    township_name = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    community_area_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.address} (PIN: {self.pin})"
