from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_property/', views.add_property, name='add_property'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('car_booking/<int:id>/', views.car_booking, name='car_booking'),
    path('manage_booking/', views.manage_booking, name='manage_booking'),
    path('manage_property/', views.manage_property, name='manage_property'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('payment/<int:id>/', views.create_payment, name='payment'),
    path('success/<int:id>/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('review/', views.review_ratings, name='review'),
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    path('search/', views.search_point, name='search'),
    path('user/', views.user_buyer, name='user_roll'),
    #path('session/', views.setsession, name='setsession'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
