from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Property, Booking

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'address', 'description', 'rent_amount', 'available_date', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['property', 'start_date', 'end_date']