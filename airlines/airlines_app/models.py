from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

title = namedtuple('title', 'id name')
TITLES = (
    title(1, "Mr"),
    title(2, "Mrs"),
    title(3, "Miss")
)


class MyUser(AbstractUser):
    title = models.IntegerField(choices=TITLES, null=True)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=64, null=True)  # dodac liste
    phone_number = models.CharField(max_length=9, null=True)


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    iata_code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    number = models.CharField(max_length=64, unique=True)
    city_from = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='city_from')
    city_to = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='city_to')
    depart = models.DateTimeField()
    arrival = models.DateTimeField()
    fare = models.DecimalField(decimal_places=2, max_digits=7)
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.number


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    total_cost = models.DecimalField(decimal_places=2, max_digits=7)
    paid = models.BooleanField(default=False)


class Passenger(models.Model):
    title = models.IntegerField(choices=TITLES)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    age_range = models.CharField(max_length=16, null=True)
    nationality = models.CharField(max_length=64)
    passport = models.CharField(max_length=64, null=True, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Luggage(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    luggage_type = models.CharField(max_length=64)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)


class Payment(models.Model):
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    card_holder_name = models.CharField(max_length=64)
    cvv = models.CharField(max_length=3)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
