from django.contrib import admin
from .models import User, Property, Booking

admin.site.register(User)
admin.site.register(Property)
admin.site.register(Booking)
