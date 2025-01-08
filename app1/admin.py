from django.contrib import admin
from .models import User, Property, Booking, Review, Payment

admin.site.register(User)
admin.site.register(Property)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display =['id','user','total_cost']


@admin.register(Review)
class Reviewadmin(admin.ModelAdmin):
    list_display = ['review','rating']

@admin.register(Payment)
class Paymentadmin(admin.ModelAdmin):
    list_display = ['booking','status']
