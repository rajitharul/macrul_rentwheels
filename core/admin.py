from django.contrib import admin
from .models import Vehicle, Driver, Rental, Review

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'model', 'year', 'vehicle_type', 'daily_rate', 'is_available')
    list_filter = ('vehicle_type', 'is_available', 'year')
    search_fields = ('name', 'make', 'model', 'license_plate')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'experience_years', 'is_available')
    list_filter = ('is_available', 'experience_years')
    search_fields = ('user__username', 'user__email', 'license_number')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vehicle', 'driver', 'start_date', 'end_date', 'status', 'total_cost')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('customer__username', 'vehicle__name', 'driver__user__username')
    readonly_fields = ('total_cost',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rental', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('rental__customer__username', 'comment')
