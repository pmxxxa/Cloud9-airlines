from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from airlines_app.models import City, Country, Airport, Flight, Luggage, Booking, Passenger, Payment
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

admin.site.register(MyUser, UserAdmin)



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields if field.name != 'id']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields if field.name != 'id']


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Airport._meta.fields if field.name != 'id']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.fields if field.name != 'id']


@admin.register(Luggage)
class LuggageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Luggage._meta.fields if field.name != 'id']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Booking._meta.fields if field.name != 'id']


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Passenger._meta.fields if field.name != 'id']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields if field.name != 'id']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email', 'phone_number', 'title', 'first_name', 'last_name',
                  'date_of_birth', 'nationality')
