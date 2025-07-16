from django.db import models
from location_field.models.plain import PlainLocationField
# Create your models here.

food_access_choices = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Limited', 'Limited'),
]

class FoodDesertSubmission(models.Model):
    location = models.CharField(max_length=100)
    coordinates = PlainLocationField(based_fields=['location'], zoom=7)
    food_access = models.CharField(max_length=100, choices=food_access_choices)




    def __str__(self):
        return self.location