from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from bookings.models import Booking

from .models import Vehicle
from .permissions import IsStaffUser
from .serializers import VehicleSerializer

# Create your views here.


class VehicleListCreateView(generics.ListCreateAPIView):

    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.all()

        # Filter by vehicle_type if provided in query parameters
        vehicle_type = self.request.query_params.get("vehicle_type")
        available = self.request.query_params.get("available")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
        if available == "true":
            queryset = queryset.filter(is_available=True)
        if available == "false":
            queryset = queryset.filter(is_available=False)
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)
        if start_date and end_date:
            queryset = queryset.filter(is_available=True).exclude(
                bookings__start_date__lt=end_date,
                bookings__end_date__gt=start_date,
                bookings__status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
            )

        return queryset


    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsStaffUser()]


class VehicleDetailView(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsStaffUser()]