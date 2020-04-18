from datetime import datetime, date

from django.core.exceptions import ValidationError
import django.contrib.auth
from django import forms
from django.contrib.auth.forms import UserCreationForm

from airlines_app.admin import UserChangeForm
from airlines_app.models import Flight, MyUser, Passenger, TITLES


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'title', 'first_name', 'last_name',
                  'date_of_birth', 'nationality']
        widgets = {'date_of_birth': DateInput()}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and MyUser.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email already exists.')
        return email

    def clean(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth > date.today():
            raise forms.ValidationError(u'Select the correct date.')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)

    def clean(self):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = django.contrib.auth.authenticate(username=username, password=password)

        if user:
            self.cleaned_data['user'] = user
        else:
            raise ValidationError('Incorrect username or password')


class EditProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        widgets = {'date_of_birth': DateInput()}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and MyUser.objects.filter(email=email).exclude(is_active=True).exists():
            raise forms.ValidationError(f'This email already exists.')
        return email


class ChangePasswordForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput)
    old_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean(self):

        user = MyUser.objects.filter(username=self.cleaned_data['username']).first()

        if user is None:
            raise forms.ValidationError('No such user')

        if not django.contrib.auth.authenticate(username=user.username, password=self.cleaned_data['old_password']):
            raise forms.ValidationError('Incorrect old password')

        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('The repeated password does not match')


class SearchFlightForm(forms.Form):
    city_from = forms.CharField(label="From", widget=forms.Select)
    city_to = forms.CharField(label="To", widget=forms.Select)
    depart = forms.DateField(widget=DateInput, required=False)
    adults = forms.IntegerField(min_value=1, max_value=10, initial=1, help_text='16+ at the time of travel')
    teens = forms.IntegerField(min_value=0, max_value=10, initial=0, help_text='12-15 years at the time of travel')
    children = forms.IntegerField(min_value=0, max_value=10, initial=0, help_text='2-11 years at the time of travel')
    infants = forms.IntegerField(min_value=0, max_value=10, initial=0, help_text='Under 2 years at the time of travel')

    help_texts = {'adults': '16+ at the time of travel'}

    def clean(self):
        city_from = self.cleaned_data['city_from']
        city_to = self.cleaned_data['city_to']
        depart = self.cleaned_data['depart']
        if depart:
            flights = Flight.objects.filter(city_from=city_from).filter(city_to=city_to).filter(depart=depart)
            if depart < date.today():
                raise forms.ValidationError('You can not book past flights')
        else:
            flights = Flight.objects.filter(city_from=city_from).filter(city_to=city_to)
        if flights is None:
            raise forms.ValidationError('No flights available')


class PassengerForm(forms.Form):
    age_range = forms.CharField(widget=forms.HiddenInput)
    flight_number = forms.CharField(widget=forms.HiddenInput)
    title = forms.ChoiceField(choices=TITLES)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    date_of_birth = forms.DateField(widget=DateInput)
    nationality = forms.CharField(max_length=64)

    def clean_date_of_birth(self):
        age_range = self.cleaned_data.get('age_range')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        flight_number = self.cleaned_data.get('flight_number')
        print(flight_number)
        flight = Flight.objects.get(number=flight_number)
        if age_range == "adult":
            if (flight.depart.date() - date_of_birth).total_seconds() / 365 < 1382400:
                print("datyyyy", (flight.depart.date() - date_of_birth).total_seconds() / 365)
                raise forms.ValidationError('No flights available')


class LuggageForm(forms.Form):
    small_bag = forms.IntegerField(label="Small Bag", help_text='included', min_value=1, max_value=1, initial=1)
    priority_2_cabin_bags = forms.IntegerField(label="Priority & 2 Cabin Bags", help_text='10 €', min_value=0,
                                               max_value=1, initial=0)
    ten_kg_check_in_bag = forms.IntegerField(label="10kg Check-in Bag", help_text='15 €', min_value=0, max_value=1,
                                             initial=0)
    twenty_kg_check_in_bag = forms.IntegerField(label="20kg Check-in Bag", help_text='25 €', min_value=0, max_value=3,
                                                initial=0)


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    expiration_date = forms.CharField(max_length=5, help_text='MM/YY')
    card_holder_name = forms.CharField(max_length=64)
    cvv = forms.CharField(max_length=3, label="CVV")


class CheckInForm(forms.Form):
    passport = forms.CharField(max_length=20)
