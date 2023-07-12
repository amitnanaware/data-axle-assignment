from django.contrib.gis.db import models
from django.contrib.auth.models import User


class ParkingSpot(models.Model):
    location = models.PointField()
    address = models.CharField(max_length=255)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Parking Spot at {self.address}"

    def calculate_price(self, hours):
        return self.price_per_hour * hours



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    hours = models.IntegerField()
    reservation_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def calculate_price(self):
        return self.parking_spot.calculate_price(self.hours)
