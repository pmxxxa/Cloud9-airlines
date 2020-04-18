from datetime import datetime, date, timezone

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView

from airlines_app.forms import LoginForm, ChangePasswordForm, SignUpForm, SearchFlightForm, EditProfileForm, \
    BookingForm, PassengerForm, LuggageForm, PaymentForm, CheckInForm
from airlines_app.models import MyUser, City, Flight, Passenger, Booking, Luggage, Payment


class MainPageView(View):

    def get(self, request):
        search = False
        form = SearchFlightForm()
        form.fields['city_from'].widget.choices = [(x.id, x.name) for x in City.objects.all().order_by('name')]
        form.fields['city_to'].widget.choices = [(x.id, x.name) for x in City.objects.all().order_by('name')]
        return render(request, "main_page.html", {'form': form, 'search': search})

    def post(self, request):
        search = False
        warning = False
        form = SearchFlightForm(request.POST)
        form.fields['city_from'].widget.choices = [(x.id, x.name) for x in City.objects.all().order_by('name')]
        form.fields['city_to'].widget.choices = [(x.id, x.name) for x in City.objects.all().order_by('name')]
        if form.is_valid():
            # trip = form.cleaned_data.get('trip')
            city_from = form.cleaned_data.get('city_from')
            city_to = form.cleaned_data.get('city_to')
            depart = form.cleaned_data.get('depart')
            adults = int(form.cleaned_data.get('adults'))
            teens = int(form.cleaned_data.get('teens'))
            children = int(form.cleaned_data.get('children'))
            infants = int(form.cleaned_data.get('infants'))
            cf = City.objects.get(pk=city_from)
            ct = City.objects.get(pk=city_to)
            if depart:
                flights = Flight.objects.filter(city_from=city_from).filter(city_to=city_to).filter(
                    available_seats__gte=adults + teens + children).filter(depart__icontains=depart)
            else:
                flights = Flight.objects.filter(city_from=city_from).filter(
                    available_seats__gte=adults + teens + children).filter(city_to=city_to).filter(
                    depart__gt=datetime.now())
            if flights:
                search = True
                for i in flights:
                    if i.available_seats == (adults + teens + children) or i.available_seats < 6:
                        warning = True
            request.session['adults'] = adults
            return render(request, 'main_page.html',
                          {'form': form, 'flights': flights, 'search': search, 'cf': cf, 'ct': ct, 'adults': adults,
                           'teens': teens, 'children': children, 'infants': infants, 'warning': warning})
        else:
            return render(request, 'main_page.html', {'form': form, 'search': search})


class SignUpView(View):
    def get(self, request):
        return render(request, 'sing_up.html', {
            'form': SignUpForm()
        })

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Welcome {first_name} to myCloud9!')
            return redirect('/')
        else:
            return render(request, 'sing_up.html', {'form': form})


class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('/')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)
        return render(request, 'edit_profile.html', {
            'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        user = request.user
        if form.is_valid():
            user.save()
            return render(request, 'user_profile.html')
        else:
            return render(request, 'edit_profile.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request, username):
        if request.user == MyUser.objects.get(username=username):
            return render(request, 'change_password.html', {
                'form': ChangePasswordForm(initial={'username': username
                                                    }),
            })
        else:
            return redirect('/')

    def post(self, request, username):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponse('Password changed')
        else:
            return render(request, 'change_password.html', {
                'form': form,
            })


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user_profile.html', {'user': user})


class BookingView(LoginRequiredMixin, View):
    def get(self, request, flight_number, adults, teens, children, infants):
        aaa = request.session.get('adults')
        print("AAAAAA", aaa)
        flight = Flight.objects.get(number=flight_number)
        passengers = int(adults + teens + children + infants)
        print(passengers)
        list_form = []
        j = 1
        for j in range(int(passengers)):
            list_form.append(PassengerForm(prefix=str(j)))
            print("get prefix", j)
            j += 1
        return render(request, 'booking.html', {'flight': flight, 'list_form': list_form, 'passengers': passengers
                                                })

    def post(self, request, flight_number, adults, teens, children, infants):
        form = BookingForm(request.POST)
        passengers = int(adults + teens + children + infants)
        # if not valid
        list_form = []
        k = 1
        for i in range(int(passengers)):
            list_form.append(PassengerForm(prefix=str(k)))
            k += 1
        ###
        list_form2 = []
        n = 1
        for i in range(int(passengers)):
            list_form2.append(PassengerForm(request.POST, prefix=str(n)))
            print("post prefix", n)
            n += 1
        print(list_form2)
        ###
        flight = Flight.objects.get(number=flight_number)
        for i in range(int(passengers)):
            if not list_form2[i].is_valid():
                return render(request, 'booking.html',
                              {'flight': flight, 'list_form': list_form, 'passengers': passengers
                               })
        user = request.user
        total_cost = (int(adults) + int(teens)) * flight.fare + int(children) * flight.fare + int(infants) * 25
        print(flight, user, total_cost)
        booking = Booking.objects.create(flight=flight, user=user, total_cost=total_cost)
        print(booking)
        seats = int(adults + teens + children)
        booking.flight.available_seats = int(booking.flight.available_seats) - seats
        booking.save()
        if adults > 0:
            for i in range(int(passengers)):
                title = list_form2[i].cleaned_data.get('title')
                first_name = list_form2[i].cleaned_data.get('first_name')
                last_name = list_form2[i].cleaned_data.get('last_name')
                date_of_birth = list_form2[i].cleaned_data.get('date_of_birth')
                nationality = list_form2[i].cleaned_data.get('nationality')
                passenger = Passenger.objects.create(title=title, first_name=first_name, last_name=last_name,
                                                     date_of_birth=date_of_birth, nationality=nationality,
                                                     flight=flight, booking=booking)
                age = "adult"
                print(passenger)
            """
        for i in range(int(passengers)):
            title = list_form2[i].cleaned_data.get('title')
            first_name = list_form2[i].cleaned_data.get('first_name')
            last_name = list_form2[i].cleaned_data.get('last_name')
            date_of_birth = list_form2[i].cleaned_data.get('date_of_birth')
            nationality = list_form2[i].cleaned_data.get('nationality')
            passenger = Passenger.objects.create(title=title, first_name=first_name, last_name=last_name,
                                                 date_of_birth=date_of_birth, nationality=nationality,
                                                 flight=flight, booking=booking)
            print(passenger)
            if passenger is None:
                return render(request, 'booking.html',
                              {'flight': flight, 'list_form': list_form, 'passengers': passengers
                               })"""
            booking_id = int(booking.id)
        return redirect(f'/luggage/{booking_id}/')


class MyBookingsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        past_trips = []
        upcoming_trips = []
        bookings = Booking.objects.filter(user=user)

        for b in bookings:
            if b.flight.depart < datetime.now(timezone.utc):
                past_trips.append(b)
            else:
                upcoming_trips.append(b)
        return render(request, 'my_bookings.html',
                      {'user': user, 'past_trips': past_trips, 'upcoming_trips': upcoming_trips})


class BookingDetailsView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        user = request.user
        booking = Booking.objects.get(pk=booking_id)
        passengers = Passenger.objects.filter(booking=booking)
        luggage = Luggage.objects.filter(booking=booking)
        print(user, booking)
        check_in_avalible = False
        for i in passengers:
            if (booking.flight.depart - datetime.now(
                    timezone.utc)).total_seconds() <= 172800 and booking.paid == True and i.checked_in == False:
                check_in_avalible = True
        return render(request, 'booking_details.html',
                      {'user': user, 'booking': booking, 'passengers': passengers, 'luggage': luggage,
                       'check_in_avalible': check_in_avalible})


class LuggageView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        passengers = Passenger.objects.filter(booking=booking)
        list_get = []
        for i in passengers:
            list_get.append(LuggageForm(prefix=str(i)))
            print(i)
        return render(request, 'luggage.html', {'list_get': list_get, 'passengers': passengers, 'booking': booking})

    def post(self, request, booking_id):
        user = request.user
        booking = Booking.objects.get(pk=booking_id)
        passengers = Passenger.objects.filter(booking=booking)
        for i in passengers:
            print("post prefix", i)
            if not LuggageForm(request.POST, prefix=str(i)).is_valid():
                return redirect(f'/luggage/{booking_id}/')
        print('forms valid')
        cost = 0
        for i in passengers:
            form = LuggageForm(request.POST, prefix=str(i))
            print(form)
            small_bag = int(form.cleaned_data.get('small_bag'))
            if small_bag == 1:
                for j in range(small_bag):
                    Luggage.objects.create(user=user, luggage_type='small_bag', passenger=i, booking=booking)
            priority_2_cabin_bags = int(form.cleaned_data.get('priority_2_cabin_bags'))
            print(priority_2_cabin_bags)
            if priority_2_cabin_bags == 1:
                Luggage.objects.create(user=user, luggage_type='Priority & 2 Cabin Bags', passenger=i,
                                       booking=booking)
                cost += 10
            ten_kg_check_in_bag = int(form.cleaned_data.get('ten_kg_check_in_bag'))
            print(ten_kg_check_in_bag)
            if ten_kg_check_in_bag == 1:
                Luggage.objects.create(user=user, luggage_type='10kg Check-in Bag', passenger=i, booking=booking)
                cost += 15
            twenty_kg_check_in_bag = int(form.cleaned_data.get('twenty_kg_check_in_bag'))
            print(twenty_kg_check_in_bag)
            if twenty_kg_check_in_bag > 0:
                for j in range(twenty_kg_check_in_bag):
                    Luggage.objects.create(user=user, luggage_type='20kg Check-in Bag', passenger=i, booking=booking)
                    cost += (25 * ten_kg_check_in_bag)
        booking.total_cost = float(booking.total_cost) + cost
        booking.save()
        if 'pay_now' in request.POST:
            return redirect(f'/payment/{booking_id}/')
        elif 'pay_later' in request.POST:
            return redirect(f'/booking_details/{booking_id}/')


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        passengers = len(Passenger.objects.filter(booking=booking))
        priority_2_cabin_bags = len(
            Luggage.objects.filter(booking=booking).filter(luggage_type='Priority & 2 Cabin Bags'))
        ten_kg_check_in_bag = len(Luggage.objects.filter(booking=booking).filter(luggage_type='10kg Check-in Bag'))
        twenty_kg_check_in_bag = len(
            Luggage.objects.filter(booking=booking).filter(luggage_type='20kg Check-in Bag'))
        luggage = int(priority_2_cabin_bags + ten_kg_check_in_bag + twenty_kg_check_in_bag)
        return render(request, 'payment.html', {'form': PaymentForm(), 'booking': booking, 'passengers': passengers,
                                                'priority_2_cabin_bags': priority_2_cabin_bags,
                                                'ten_kg_check_in_bag': ten_kg_check_in_bag,
                                                'twenty_kg_check_in_bag': twenty_kg_check_in_bag, 'luggage': luggage})

    def post(self, request, booking_id):
        form = PaymentForm(request.POST)
        if form.is_valid():
            user = request.user
            booking = Booking.objects.get(pk=booking_id)
            card_number = form.cleaned_data.get('card_number')
            expiration_date = form.cleaned_data.get('expiration_date')
            card_holder_name = form.cleaned_data.get('card_holder_name')
            cvv = form.cleaned_data.get('cvv')
            print(card_number, expiration_date, card_holder_name, cvv)
            Payment.objects.create(card_number=card_number, expiration_date=expiration_date,
                                   card_holder_name=card_holder_name, cvv=cvv, user=user, booking=booking)
            booking.paid = True
            booking.save()
            return redirect(f'/booking_details/{booking_id}/')
        else:
            return redirect(f'/payment/{booking_id}/')


class CheckInView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        passengers = Passenger.objects.filter(booking=booking)
        list_get = []
        for i in passengers:
            list_get.append(CheckInForm(prefix=str(i)))
            print(i)
        return render(request, 'check_in.html', {'booking': booking, 'passengers': passengers, 'list_get': list_get})

    def post(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        passengers = Passenger.objects.filter(booking=booking)
        for i in passengers:
            print("post prefix", i)
            if not CheckInForm(request.POST, prefix=str(i)).is_valid():
                return redirect(f'/check_in/{booking_id}/')
        print('forms valid')
        for i in passengers:
            form = CheckInForm(request.POST, prefix=str(i))
            print(form)
            passport = form.cleaned_data.get('passport')
            i.passport = passport
            i.checked_in = True
            i.save()
        return redirect(f'/booking_details/{booking_id}/')
