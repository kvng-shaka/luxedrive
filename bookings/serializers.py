from django.utils import timezone
from rest_framework import serializers

from .models import Booking
from vehicles.models import Vehicle


class BookingSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True,)

    class Meta:
        model = Booking

        fields = [
            "id",
            "user",
            "vehicle",
            "vehicle_name",
            "start_date",
            "end_date",
            "pickup_location",
            "dropoff_location",
            "duration_days",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "vehicle_name",
            "duration_days",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]


    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None),)
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None),)
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError("End date must be after start date.")

            if start_date < timezone.localdate():
                raise serializers.ValidationError("Start date cannot be in the past.")

        vehicle = attrs.get("vehicle", getattr(self.instance, "vehicle", None),)
        if vehicle:
            if not vehicle.is_available:
                raise serializers.ValidationError("This vehicle is currently unavailable.")

            if (vehicle.maintenance_status != Vehicle.MaintenanceStatus.OPERATIONAL):
                raise serializers.ValidationError("This vehicle is currently under maintenance.")

        overlapping_bookings = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=[
                Booking.Status.PENDING,
                Booking.Status.CONFIRMED,
            ],
        )
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This vehicle is already booked for the selected dates.")

        return attrs


    def create(self, validated_data):
        vehicle = validated_data["vehicle"]
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        duration_days = (end_date - start_date).days
        total_amount = (vehicle.price_per_day * duration_days)

        booking = Booking.objects.create(**validated_data, duration_days=duration_days, total_amount=total_amount,)

        return booking


    def update(self, instance, validated_data):
        vehicle = validated_data.get("vehicle", instance.vehicle,)
        start_date = validated_data.get("start_date", instance.start_date,)
        end_date = validated_data.get("end_date", instance.end_date,)
        duration_days = (end_date - start_date).days
        total_amount = (vehicle.price_per_day * duration_days)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.duration_days = duration_days
        instance.total_amount = total_amount

        instance.save()

        return instance