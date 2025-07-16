from django.db import models
from django.core.validators import RegexValidator


class Property(models.Model):
    """
    Comprehensive property model based on Cook County data
    Contains location, administrative, tax, environmental, and demographic information
    """
    
    # Primary identifiers
    pin = models.CharField(max_length=20, unique=True, db_index=True, 
                          help_text="Property Identification Number")
    pin10 = models.CharField(max_length=15, db_index=True,
                           help_text="10-digit PIN format")
    year = models.IntegerField(help_text="Tax year")
    class_code = models.CharField(max_length=10, help_text="Property class code")
    row_id = models.CharField(max_length=50, unique=True, help_text="Unique row identifier")
    
    # Location data
    longitude = models.FloatField(help_text="Longitude coordinate")
    latitude = models.FloatField(help_text="Latitude coordinate")
    x_3435 = models.FloatField(null=True, blank=True, help_text="X coordinate in Illinois State Plane")
    y_3435 = models.FloatField(null=True, blank=True, help_text="Y coordinate in Illinois State Plane")
    zip_code = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    
    # Administrative divisions
    triad_name = models.CharField(max_length=50, help_text="Triad name")
    triad_code = models.IntegerField(help_text="Triad code")
    township_name = models.CharField(max_length=50, help_text="Township name")
    township_code = models.IntegerField(help_text="Township code")
    nbhd_code = models.CharField(max_length=20, help_text="Neighborhood code")
    tax_code = models.CharField(max_length=20, help_text="Tax code")
    
    # Census data
    census_block_group_geoid = models.CharField(max_length=20, null=True, blank=True)
    census_block_geoid = models.CharField(max_length=20, null=True, blank=True)
    census_congressional_district_geoid = models.CharField(max_length=10, null=True, blank=True)
    census_congressional_district_num = models.IntegerField(null=True, blank=True)
    census_tract_geoid = models.CharField(max_length=20, null=True, blank=True)
    census_data_year = models.IntegerField(null=True, blank=True)
    
    # Chicago specific data
    ward_num = models.IntegerField(null=True, blank=True, help_text="Chicago ward number")
    ward_chicago_data_year = models.IntegerField(null=True, blank=True)
    chicago_community_area_num = models.IntegerField(null=True, blank=True)
    chicago_community_area_name = models.CharField(max_length=100, null=True, blank=True)
    chicago_police_district_num = models.IntegerField(null=True, blank=True)
    
    # School districts
    school_elementary_district_geoid = models.CharField(max_length=20, null=True, blank=True)
    school_elementary_district_name = models.CharField(max_length=200, null=True, blank=True)
    school_secondary_district_geoid = models.CharField(max_length=20, null=True, blank=True)
    school_secondary_district_name = models.CharField(max_length=200, null=True, blank=True)
    school_unified_district_geoid = models.CharField(max_length=20, null=True, blank=True)
    school_unified_district_name = models.CharField(max_length=200, null=True, blank=True)
    school_school_year = models.CharField(max_length=20, null=True, blank=True)
    school_data_year = models.IntegerField(null=True, blank=True)
    
    # Tax districts
    tax_municipality_num = models.CharField(max_length=20, null=True, blank=True)
    tax_municipality_name = models.CharField(max_length=100, null=True, blank=True)
    tax_school_elementary_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_school_elementary_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_school_secondary_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_school_secondary_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_community_college_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_community_college_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_fire_protection_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_fire_protection_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_library_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_library_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_park_district_num = models.CharField(max_length=20, null=True, blank=True)
    tax_park_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_tif_district_num = models.FloatField(null=True, blank=True)
    tax_tif_district_name = models.CharField(max_length=200, null=True, blank=True)
    tax_data_year = models.IntegerField(null=True, blank=True)
    
    # Environmental data
    env_flood_fema_sfha = models.BooleanField(null=True, blank=True, 
                                            help_text="FEMA Special Flood Hazard Area")
    env_flood_fema_data_year = models.IntegerField(null=True, blank=True)
    env_flood_fs_factor = models.FloatField(null=True, blank=True, 
                                          help_text="Flood factor score")
    env_flood_fs_risk_direction = models.CharField(max_length=50, null=True, blank=True)
    env_ohare_noise_contour_no_buffer_bool = models.BooleanField(null=True, blank=True)
    env_ohare_noise_contour_half_mile_buffer_bool = models.BooleanField(null=True, blank=True)
    env_airport_noise_dnl = models.FloatField(null=True, blank=True, 
                                            help_text="Airport noise level in DNL")
    
    # Economic zones
    econ_enterprise_zone_num = models.CharField(max_length=20, null=True, blank=True)
    econ_qualified_opportunity_zone_num = models.CharField(max_length=20, null=True, blank=True)
    
    # Accessibility scores
    access_cmap_walk_id = models.IntegerField(null=True, blank=True)
    access_cmap_walk_nta_score = models.FloatField(null=True, blank=True)
    access_cmap_walk_total_score = models.FloatField(null=True, blank=True)
    access_cmap_walk_data_year = models.IntegerField(null=True, blank=True)
    
    # Subdivision data
    misc_subdivision_id = models.CharField(max_length=50, null=True, blank=True)
    misc_subdivision_data_year = models.FloatField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'
        indexes = [
            models.Index(fields=['pin']),
            models.Index(fields=['zip_code']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['chicago_community_area_num']),
            models.Index(fields=['ward_num']),
            models.Index(fields=['township_name']),
        ]
        ordering = ['pin']
    
    def __str__(self):
        return f"PIN: {self.pin} - {self.chicago_community_area_name or 'Unknown Area'}"
    
    @property
    def coordinates(self):
        """Return coordinates as [longitude, latitude] for mapping"""
        return [self.longitude, self.latitude]
    
    @property
    def address_display(self):
        """Generate a display address when available"""
        parts = []
        if self.chicago_community_area_name:
            parts.append(self.chicago_community_area_name)
        if self.zip_code:
            parts.append(f"ZIP {self.zip_code}")
        return ", ".join(parts) if parts else f"PIN {self.pin}"
    
    def nearby_properties(self, radius_km=1.0):
        """Find properties within radius (in kilometers)"""
        # Simple bounding box calculation for nearby properties
        # Rough conversion: 1 degree ≈ 111 km
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.0 * abs(self.latitude))
        
        return Property.objects.filter(
            latitude__range=(self.latitude - lat_delta, self.latitude + lat_delta),
            longitude__range=(self.longitude - lon_delta, self.longitude + lon_delta)
        ).exclude(pk=self.pk)[:50]  # Limit to 50 nearby properties


class PropertySearchIndex(models.Model):
    """
    Search index for property lookup optimization
    """
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='search_index')
    search_text = models.TextField(help_text="Combined searchable text")
    
    class Meta:
        db_table = 'property_search_index'
    
    def __str__(self):
        return f"Search index for {self.property.pin}" 