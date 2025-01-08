from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import UserRegistrationForm, PropertyForm, BookingForm, Review_rating 
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Property, Booking, Review, User
from datetime import date
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q


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



# @login_required
# def user_buyer(request):
#     #user_role = request.session.get("user_role") 
#     if request.user.role == 'buyer':
#         properties = Property.objects.filter(owner=request.user)
#         return redirect('search')
#     elif request.user.role == 'admin' :
#         return redirect('manage_booking')
#     elif request.user.role == 'owner':
#         return redirect('manage_property')
#     else:
#         properties = Property.objects.all()
#     return render(request,'user.html', {'properties': properties})


def login(request):
    if request.user.is_authenticated:
        return redirect('user_roll')  

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                request.session['user_role'] = getattr(user, 'role', None)
                request.session['username'] = user.username
                # request.session['id'] = user.id
                # print(request.session["id"],"++++++++++")
                # print(request.session,"----------------------------------")
                return redirect("user_roll")
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'logout.html')

@login_required
def user_buyer(request):
    # Retrieve the user role from the session
    user_role = request.session.get('user_role')

    # Role-based redirection
    role_redirects = {
        'buyer': 'search',
        'admin': 'manage_booking',
        'owner': 'manage_property',
    }

    if user_role in role_redirects:
        return redirect(role_redirects[user_role])

    # Default case: show all properties
    properties = Property.objects.all()
    return render(request, 'user.html', {'properties': properties})

    


@login_required
def search_point(request):

    search_query = request.GET.get('search', '')  
    
    if search_query:
        if search_query.isdigit(): 
            properties = Property.objects.filter(rent_amount__gte=search_query) 
        else:
            properties = Property.objects.filter(title__icontains=search_query)  
    else:
        properties = Property.objects.all() 
    return render(request, 'search.html', {'properties': properties})



@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('manage_property')
    else:
        form = PropertyForm()
    return render(request, 'add_property.html' , {'form': form})

@login_required
def manage_property(request):
    properties = Property.objects.all()
    return render(request, 'manage_property.html', {'properties': properties})


@login_required
def update(request, id):
    property_instance = get_object_or_404(Property, id=id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            return redirect('manage_property')
    else:
        form = PropertyForm(instance=property_instance)
    return render(request, 'add_property.html', {'form': form, 'property': property_instance})


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
    #if request.user.role == 'owner':
    bookings = Booking.objects.all()
    return render(request, 'manage_booking.html', {'bookings': bookings})

@login_required
def delete(request,id):
    #if item is.Booking:
    item = get_object_or_404(Booking,id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('manage_booking') 
    return render(request, 'delete.html', {'item': item})


stripe.api_key = "sk_test_51QUm8KP6Spmdws9YmTPM0LIcOGXJO9tii8gLVWQXN6UxfyCbQUn43F0PzPrmmHAH8xzhlwyUanHmfWROhvzLEZ2200ZT8OZcCu"
def create_payment(request, id):
    data = Booking.objects.get(id=id)
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
                            "unit_amount": money * 100,
                            "product_data": {
                                "name": 'title',
                                "description": f"Booking ID: {id} ",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                #success_url=f"http://127.0.0.1:8000/success/{id}/?session_id={{CHECKOUT_SESSION_ID}}",
                success_url=f"http://127.0.0.1:8000/success/{id}/",
                cancel_url=f"http://127.0.0.1:8000/cancel/",
                #metadata={"booking_id": id}, 
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, 'payment.html', {'total_cost': data.total_cost})


def success(request, id):   
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return render(request, 'error.html', {"message": "Booking not found."})
    return render(request, 'successs.html', {"booking": booking})
    

def cancel(request,id):
    booking = get_object_or_404(Booking, id=id)
    return render(request, 'cancel.html',{'booking':booking})

@login_required
def review_ratings(request):
    if request.method == 'POST':
        form = Review_rating(request.POST)
        if form.is_valid():
                form = form.save(commit=False)
                form.save()
        #return redirect('home')
    else:
        form = Review_rating()
    return render(request, 'review.html', {'form': form})


def user_detail(request,id):                                                                                                                                                                                                                                                                                                                                                                 
    user = get_object_or_404(User, id=id)
    user_booking = user.bookings.all()
    username = user.username
    return render(request, 'user_detail.html', {'user_bookings': user_booking, 'username':username})