from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.utils import timezone

from .models import OdourReport, StudyArea


class OdourReportSerializer(serializers.ModelSerializer):

    longitude = serializers.FloatField(
        min_value=-180.0, max_value=180.0, write_only=True
    )
    latitude = serializers.FloatField(
        min_value=-90.0, max_value=90.0, write_only=True
    )
    
    intensity = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = OdourReport
        fields = [
            "id",
            "longitude",
            "latitude",
            "reported_at",
            "intensity",
            "odour_type",
            "happening_now",
            "duration",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def create(self, validated_data):
        longitude = validated_data.pop("longitude")
        latitude = validated_data.pop("latitude")

        point = Point(
            longitude,
            latitude,
            srid=4326,
        )

        study_area = StudyArea.objects.filter(
            active=True,
            boundary__contains=point,
        ).first()

        if study_area is None:
            raise serializers.ValidationError(
                {
                    "location": (
                        "This location is outside the active study area."
                    )
                }
            )

        validated_data["location"] = point
        validated_data["study_area"] = study_area
        return OdourReport.objects.create(**validated_data)
    
    def validate_reported_at(self, value):
    
            if value > timezone.now():
                raise serializers.ValidationError(
                "Reported time cannot be in the future."
            )
    
            return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["longitude"] = instance.location.x
        representation["latitude"] = instance.location.y
        return representation
    