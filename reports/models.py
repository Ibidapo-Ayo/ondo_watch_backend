from django.db import models

# Create your models here.
import uuid
from django.contrib.gis.db import models

class OdourReport(models.Model):
    ODOUR_TYPES = [
        ("sewage", "Sewage"),
        ("rotten_egg", "Rotten Egg / sulfur"),
        ("burning", "Burning / smoke"),
        ("chemical", "Chemical / industrial"),
        ("fuel_gas", "Fuel / gas"),
        ("garbage", "Garbage / waste"),
        ("other", "Other"),
    ]
    
    DURATION_CHOICES = [
         ("less_5_min", "Less than 5 minutes"),
        ("5_15_min", "5–15 minutes"),
        ("15_30_min", "15–30 minutes"),
        ("30_60_min", "30–60 minutes"),
        ("more_1_hour", "More than 1 hour"),
        ("unknown", "I don't know"),
    ]
    
    
    study_area = models.ForeignKey(
        "StudyArea",
        on_delete=models.PROTECT,
        related_name="reports",
        null=True,
        blank=True,
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.PointField(
        geography=True, 
        srid=4326,
    )
    
    reported_at = models.DateTimeField()
    intensity = models.PositiveSmallIntegerField()
    
    odour_type = models.CharField(
        max_length=30,
        choices=ODOUR_TYPES,
    )
    
    happening_now =  models.BooleanField(default=True)
    
    duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
    )
    
    description = models.TextField(
        blank=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
         return f"{self.odour_type} - {self.reported_at}"
    
class StudyArea(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Nigeria",
    )

    description = models.TextField(
        blank=True,
    )

    boundary = models.MultiPolygonField(
        geography=True,
        srid=4326,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name