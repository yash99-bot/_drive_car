from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('home/',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_property/', views.add_property, name='add_property'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('car_booking/', views.car_booking, name='car_booking'),
    path('manage_property/', views.manage_property, name='manage_property'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('payment/', views.payment, name='payment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
