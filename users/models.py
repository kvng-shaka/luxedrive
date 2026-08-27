from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        STAFF = "staff", "Staff"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER,)
    phone_number = models.CharField(max_length=20,unique=True,)

    def __str__(self):
        return self.username


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",)
    date_of_birth = models.DateField(null=True, blank=True,)
    address = models.TextField(blank=True,)

    def __str__(self):
        return f"{self.user.username}'s Profile"


