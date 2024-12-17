from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Property Owner'),
        ('buyer', 'Buyer'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    available_date = models.DateField()
    image = models.ImageField(default='hh.png')

    def __str__(self):
        return self.title
    

class Booking(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        duration = (self.end_date - self.start_date).days
        self.total_cost = self.property.rent_amount * duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.property.title} {self.total_cost}"
    

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')
    payment_method = models.CharField(max_length=20, choices=[('CARD', 'Card'), ('UPI', 'UPI')])
    created_at = models.DateTimeField(auto_now_add=True)

