"""airlines URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from airlines_app.views import MainPageView, SignUpView, LoginView, ChangePasswordView, UserProfileView, \
    EditProfileView, LogoutView, BookingView, MyBookingsView, BookingDetailsView, LuggageView, PaymentView, CheckInView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view()),
    path('sign_up/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/<str:username>/', ChangePasswordView.as_view()),
    path('my_profile/', UserProfileView.as_view()),
    path('edit_profile/', EditProfileView.as_view()),
    path('booking/<str:flight_number>/<int:adults>/<int:teens>/<int:children>/<int:infants>/', BookingView.as_view()),
    path('my_bookings/', MyBookingsView.as_view()),
    path('booking_details/<int:booking_id>/', BookingDetailsView.as_view()),
    path('luggage/<int:booking_id>/', LuggageView.as_view()),
    path('payment/<int:booking_id>/', PaymentView.as_view()),
    path('check_in/<int:booking_id>/', CheckInView.as_view()),
]
