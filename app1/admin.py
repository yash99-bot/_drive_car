from django.contrib import admin
from .models import User, Property, Booking

admin.site.register(User)
admin.site.register(Property)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display =['id','user','total_cost']
