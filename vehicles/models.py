from django.db import models

# Create your models here.



class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        SUV = "suv", "SUV"
        SEDAN = "sedan", "Sedan"
        COUPE = "coupe", "Coupe"
        CONVERTIBLE = "convertible", "Convertible"
        VAN = "van", "Van"


    class MaintenanceStatus(models.TextChoices):
        OPERATIONAL = "operational", "Operational"
        MAINTENANCE = "maintenance", "Maintenance"

    name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices,)
    description = models.TextField()
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2,)
    features = models.JSONField(default=list, blank=True,)
    image = models.ImageField(upload_to="vehicles/", blank=True, null=True,)
    is_available = models.BooleanField(default=True,)
    maintenance_status = models.CharField(max_length=20, choices=MaintenanceStatus.choices, default=MaintenanceStatus.OPERATIONAL,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name