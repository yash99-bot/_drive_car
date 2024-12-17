from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, PropertyForm, BookingForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from datetime import date
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse


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
        return redirect('manage_booking')
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
def car_booking(request,id):
    properties = Property.objects.get(id =id)
    if request.method == 'POST':
        if request.user.role == 'buyer':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)  
                booking.user = request.user  
                booking.save()
                
                #print(f"Total cost: {booking.total_cost}") 
                return redirect(reverse('payment', args=[booking.id]))
            else:
                messages.error(request, "Please select a valid date range.")
        else:
            messages.error(request, "You must be a buyer to make a booking.")
    else:
        form = BookingForm()

    return render(request, 'car_booking.html', {'form': form, 'properties': properties})


@login_required
def manage_booking(request):
    if request.user.role == 'owner':
        bookings = Booking.objects.all()
    return render(request, 'manage_booking.html', {'bookings': bookings})


def update(request):
    if request.user.role == "owner":
        return render(request, 'add_property.html')

@login_required
def delete(request, id):
    item = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('manage_booking') 
    return render(request, 'delete.html', {'item': item})






stripe.api_key = "sk_test_51QUm8KP6Spmdws9YmTPM0LIcOGXJO9tii8gLVWQXN6UxfyCbQUn43F0PzPrmmHAH8xzhlwyUanHmfWROhvzLEZ2200ZT8OZcCu"
def create_payment(request,id):
    data = Booking.objects.get(id = id)
    if request.method == "POST":
        amount = request.POST['total_cost']
        amount = float(amount)
        money = int(amount)
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "unit_amount": money *100,
                            "product_data": {
                                "name": "title",
                                "description": f"Payment for booking ID: {id}", 
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"http://127.0.0.1:8000/success/",
                cancel_url=f"http://127.0.0.1:8000/cancel/",
            )
            return redirect(session.url, code=303) 
        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    return render(request, 'payment.html',  {'total_cost': data.total_cost,})


def success(request):
    return render(request, 'successs.html')
def cancel(request):
    return render(request, 'cancel.html')