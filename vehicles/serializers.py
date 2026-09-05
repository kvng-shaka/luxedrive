from rest_framework import serializers

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id", "name", "vehicle_type", "description", "year", "price_per_day",
            "features", "image", "is_available", "maintenance_status", "created_at", "updated_at",
        ]

        read_only_fields = [
            "id", "created_at", "updated_at",
        ]