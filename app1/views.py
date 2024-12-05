from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, PropertyForm, BookingForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from datetime import date

def home(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm
    return render(request, 'register.html', {'form':form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    return render(request, 'logout.html')

def update(request):
    return render(request, 'add_property.html')

def delete(request):
    return render(request, 'add_property.html')



@login_required
def dashboard(request):
    properties = Property.objects.all()

    title = request.GET.get('title')
    rent_amount = request.GET.get('rent_amount')

    properties = properties.order_by('title', 'rent_amount')
   
    if title:
        properties = properties.filter(title__icontains=title)
    if rent_amount:
        properties = properties.filter(rent_amount__gte=rent_amount)

    if request.user.role == 'owner':
        properties = properties.filter(owner=request.user)
    elif request.user.role == 'admin':
        pass
    else:
        properties = properties.all()
    return render(request, 'dashboard.html', {'properties': properties})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('add_property')
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})


@login_required
def car_booking(request):
    properties = Property.objects.all()
    if request.method == 'POST':
        if request.user.role == 'buyer':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)  
                booking.user = request.user  
                booking.save()
                print(f"Total cost: {booking.total_cost}") 
                messages.success(request, f"Your booking is successful. Total cost: {booking.total_cost}")
                return redirect('payment')
            else:
                messages.error(request, "Please select a valid date range.")
        else:
            messages.error(request, "You must be a buyer to make a booking.")
    else:
        form = BookingForm()

    return render(request, 'car_booking.html', {'form': form, 'properties': properties})

def payment(request):
    return render(request, 'payment.html')


@login_required
def manage_property(request):
    if request.user.role == 'owner':
        bookings = Booking.objects.filter(property__owner=request.user)

        return render(request, 'manage_property.html', {'bookings': bookings})
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

