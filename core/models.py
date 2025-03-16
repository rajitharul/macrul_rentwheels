from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('luxury', 'Luxury'),
    ]

    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"

class Rental(models.Model):
    RENTAL_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='pending')
    rental_id = models.CharField(max_length=6, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.get_full_name()} - {self.vehicle} ({self.rental_id})"

    @property
    def total_cost(self):
        duration = self.end_date - self.start_date
        days = duration.days + (duration.seconds / 86400)  # Include partial days
        return round(days * self.vehicle.daily_rate, 2)

class GuestRental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Guest Rental {self.id} - {self.full_name} - {self.vehicle}"

    def calculate_total_cost(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            return self.vehicle.daily_rate * days
        return 0

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.calculate_total_cost()
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        super().save(*args, **kwargs)

    def generate_confirmation_code(self):
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while GuestRental.objects.filter(confirmation_code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code

class Review(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.rental}"
