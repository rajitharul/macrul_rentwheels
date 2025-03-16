from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('rentals/', views.my_rentals, name='my_rentals'),
    path('rentals/<int:pk>/', views.rental_detail, name='rental_detail'),
    path('rentals/<int:pk>/cancel/', views.cancel_rental, name='cancel_rental'),
    path('rentals/<int:pk>/confirm/', views.confirm_rental, name='confirm_rental'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('rentals/<int:pk>/review/', views.add_review, name='add_review'),
    path('vehicles/register/', views.register_vehicle, name='register_vehicle'),
    
    # Management URLs
    path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('management/rentals/', views.admin_rentals, name='admin_rentals'),
    path('management/vehicles/', views.admin_vehicles, name='admin_vehicles'),
    path('management/vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('management/vehicles/<int:pk>/toggle/', views.toggle_vehicle, name='toggle_vehicle'),
] 