from django.conf import settings
from django.db import models

from vehicles.models import Vehicle

# Create your models here.


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings",)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name="bookings",)
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    dropoff_location = models.CharField(max_length=255, null=True, blank=True)
    duration_days = models.PositiveIntegerField(editable=False, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.vehicle.name} - "
            f"{self.start_date} to {self.end_date}"
        )