from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Vehicle, Rental, Review
from .forms import RentalForm, ReviewForm, ProfileForm, VehicleForm

def home(request):
    featured_vehicles = Vehicle.objects.filter(is_available=True)[:6]
    return render(request, 'core/home.html', {
        'featured_vehicles': featured_vehicles
    })

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    
    # Filter by vehicle type
    vehicle_type = request.GET.get('type')
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        vehicles = vehicles.filter(daily_rate__gte=min_price)
    if max_price:
        vehicles = vehicles.filter(daily_rate__lte=max_price)
    
    # Filter by availability
    available = request.GET.get('available')
    if available:
        vehicles = vehicles.filter(is_available=True)
    
    # Search by name, make, or model
    search = request.GET.get('search')
    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) |
            Q(make__icontains=search) |
            Q(model__icontains=search)
        )
    
    return render(request, 'core/vehicle_list.html', {
        'vehicles': vehicles
    })

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    form = RentalForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.customer = request.user
            rental.vehicle = vehicle
            rental.save()
            messages.success(request, 'Rental request submitted successfully!')
            return redirect('core:rental_detail', pk=rental.pk)
    
    return render(request, 'core/vehicle_detail.html', {
        'vehicle': vehicle,
        'form': form
    })

@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'core/my_rentals.html', {
        'rentals': rentals
    })

@login_required
def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk, customer=request.user)
    return render(request, 'core/rental_detail.html', {
        'rental': rental
    })

@login_required
def cancel_rental(request, pk):
    rental = get_object_or_404(Rental, pk=pk, customer=request.user)
    
    if rental.status == 'pending' or rental.status == 'confirmed':
        rental.status = 'cancelled'
        rental.save()
        messages.success(request, 'Rental cancelled successfully.')
    else:
        messages.error(request, 'This rental cannot be cancelled.')
    
    return redirect('core:rental_detail', pk=pk)

@login_required
def profile(request):
    rentals = Rental.objects.filter(customer=request.user)
    total_rentals = rentals.count()
    active_rentals = rentals.filter(status='active').count()
    completed_rentals = rentals.filter(status='completed').count()
    
    return render(request, 'core/profile.html', {
        'total_rentals': total_rentals,
        'active_rentals': active_rentals,
        'completed_rentals': completed_rentals
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('core:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'core/edit_profile.html', {
        'form': form
    })

@login_required
def add_review(request, pk):
    rental = get_object_or_404(Rental, pk=pk, customer=request.user)
    
    if rental.status != 'completed':
        messages.error(request, 'You can only review completed rentals.')
        return redirect('core:rental_detail', pk=pk)
    
    if hasattr(rental, 'review'):
        messages.error(request, 'You have already reviewed this rental.')
        return redirect('core:rental_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.rental = rental
            review.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('core:rental_detail', pk=pk)
    else:
        form = ReviewForm()
    
    return render(request, 'core/add_review.html', {
        'form': form,
        'rental': rental
    })

@login_required
def register_vehicle(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to register vehicles.')
        return redirect('core:home')
        
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle.name} has been registered successfully.')
            return redirect('core:vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'core/register_vehicle.html', {
        'form': form,
        'title': 'Register New Vehicle'
    })

@login_required
def confirm_rental(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to confirm rentals.')
        return redirect('core:home')
    
    rental = get_object_or_404(Rental, pk=pk)
    if rental.status == 'pending':
        rental.status = 'confirmed'
        rental.save()
        messages.success(request, 'Rental confirmed successfully.')
    else:
        messages.error(request, 'This rental cannot be confirmed.')
    
    return redirect('core:rental_detail', pk=pk)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('core:home')
    
    # Get statistics
    pending_rentals_count = Rental.objects.filter(status='pending').count()
    active_rentals_count = Rental.objects.filter(status='active').count()
    total_vehicles = Vehicle.objects.count()
    total_users = User.objects.count()
    
    # Get recent rentals
    recent_rentals = Rental.objects.all().order_by('-created_at')[:5]
    
    # Get available vehicles
    available_vehicles = Vehicle.objects.filter(is_available=True)[:5]
    
    return render(request, 'core/admin_dashboard.html', {
        'pending_rentals_count': pending_rentals_count,
        'active_rentals_count': active_rentals_count,
        'total_vehicles': total_vehicles,
        'total_users': total_users,
        'recent_rentals': recent_rentals,
        'available_vehicles': available_vehicles,
    })

@login_required
def admin_rentals(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    rentals = Rental.objects.all().order_by('-created_at')
    
    if status:
        rentals = rentals.filter(status=status)
    
    if search:
        rentals = rentals.filter(
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(vehicle__name__icontains=search)
        )
    
    return render(request, 'core/admin_rentals.html', {
        'rentals': rentals,
        'current_status': status,
        'search_query': search,
    })

@login_required
def admin_vehicles(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    vehicle_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    availability = request.GET.get('available', '')
    
    vehicles = Vehicle.objects.all().order_by('-created_at')
    
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    
    if availability:
        is_available = availability == 'true'
        vehicles = vehicles.filter(is_available=is_available)
    
    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) |
            Q(make__icontains=search) |
            Q(model__icontains=search)
        )
    
    return render(request, 'core/admin_vehicles.html', {
        'vehicles': vehicles,
        'current_type': vehicle_type,
        'current_availability': availability,
        'search_query': search,
    })

@login_required
def edit_vehicle(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit vehicles.')
        return redirect('core:home')
    
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vehicle {vehicle.name} has been updated successfully.')
            return redirect('core:admin_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'core/edit_vehicle.html', {
        'form': form,
        'vehicle': vehicle,
        'title': 'Edit Vehicle'
    })

@login_required
def toggle_vehicle(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to modify vehicles.')
        return redirect('core:home')
    
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.is_available = not vehicle.is_available
    vehicle.save()
    
    messages.success(request, f'Vehicle {vehicle.name} has been marked as {"available" if vehicle.is_available else "unavailable"}.')
    return redirect('core:admin_vehicles')
