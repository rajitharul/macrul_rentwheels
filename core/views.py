from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
from django.contrib.auth import authenticate
import random
import string
import logging
from .models import Vehicle, Rental, Review, GuestRental
from .forms import RentalForm, ReviewForm, ProfileForm, VehicleForm, GuestRentalForm

logger = logging.getLogger(__name__)

def generate_rental_id():
    chars = string.ascii_uppercase + string.digits
    while True:
        rental_id = ''.join(random.choices(chars, k=6))
        if not Rental.objects.filter(rental_id=rental_id).exists():
            return rental_id

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
    rental_form = RentalForm()
    guest_form = GuestRentalForm()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = RentalForm(request.POST)
            if form.is_valid():
                rental = form.save(commit=False)
                rental.customer = request.user
                rental.vehicle = vehicle
                rental.rental_id = generate_rental_id()
                rental.save()
                messages.success(request, f'Rental request submitted successfully! Your Rental ID is: {rental.rental_id}')
                return redirect('core:vehicle_detail', pk=vehicle.pk)
        else:
            form = GuestRentalForm(request.POST)
            print("Form data:", request.POST)  # Debug print
            
            if form.is_valid():
                print("Form is valid")  # Debug print
                try:
                    # Check if user already exists
                    phone_number = form.cleaned_data['phone_number']
                    if User.objects.filter(username=phone_number).exists():
                        messages.error(request, 'An account with this phone number already exists. Please login first.')
                        return redirect('core:vehicle_detail', pk=vehicle.pk)
                    
                    print("Creating user...")  # Debug print
                    # Create new user account
                    full_name = form.cleaned_data['full_name']
                    first_name = full_name.split()[0] if full_name else ''
                    last_name = ' '.join(full_name.split()[1:]) if full_name and len(full_name.split()) > 1 else ''
                    
                    user = User.objects.create_user(
                        username=phone_number,
                        email=form.cleaned_data.get('email', ''),
                        password=form.cleaned_data.get('password', ''),
                        first_name=first_name,
                        last_name=last_name
                    )
                    print("User created:", user)  # Debug print
                    
                    # Create rental with rental ID
                    rental_id = generate_rental_id()
                    rental = Rental.objects.create(
                        customer=user,
                        vehicle=vehicle,
                        start_date=form.cleaned_data['start_date'],
                        end_date=form.cleaned_data['end_date'],
                        pickup_location=form.cleaned_data.get('pickup_location', ''),
                        dropoff_location=form.cleaned_data.get('dropoff_location', ''),
                        status='pending',
                        rental_id=rental_id
                    )
                    print("Rental created:", rental)  # Debug print
                    
                    # Authenticate and log in the user
                    authenticated_user = authenticate(
                        request,
                        username=phone_number,
                        password=form.cleaned_data.get('password', '')
                    )
                    if authenticated_user:
                        login(request, authenticated_user)
                        messages.success(request, 'Success! Your rental has been submitted.\n' + 
                                               f'Rental ID: {rental_id}\n' +
                                               f'Login Phone: {phone_number}')
                    else:
                        messages.warning(request, 'Account created but login failed. Please login manually.')
                    return redirect('core:vehicle_detail', pk=vehicle.pk)
                except Exception as e:
                    print("Error:", str(e))  # Debug print
                    logger.error(f"Error creating rental: {str(e)}")
                    messages.error(request, str(e))  # Show the actual error
                    return redirect('core:vehicle_detail', pk=vehicle.pk)
            else:
                print("Form errors:", form.errors)  # Debug print
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return redirect('core:vehicle_detail', pk=vehicle.pk)
    
    return render(request, 'core/vehicle_detail.html', {
        'vehicle': vehicle,
        'rental_form': rental_form,
        'guest_form': guest_form
    })

@login_required
def my_rentals(request):
    # Get all rentals for the user, ordered by most recent first
    rentals = Rental.objects.filter(
        customer=request.user
    ).select_related(
        'vehicle'  # Optimize by fetching vehicle data in same query
    ).order_by('-created_at')
    
    # Split rentals by status
    active_rentals = [r for r in rentals if r.status in ['pending', 'approved', 'active']]
    past_rentals = [r for r in rentals if r.status in ['completed', 'cancelled']]
    
    return render(request, 'core/my_rentals.html', {
        'active_rentals': active_rentals,
        'past_rentals': past_rentals,
        'total_rentals': len(rentals)
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
    rentals = Rental.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'rentals': rentals,
        'user': request.user
    }
    return render(request, 'core/profile.html', context)

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
    
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(is_available=True).count()
    total_rentals = Rental.objects.count()
    pending_rentals = Rental.objects.filter(status='pending').count()
    pending_guest_rentals = GuestRental.objects.filter(status='pending').count()
    
    context = {
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'total_rentals': total_rentals,
        'pending_rentals': pending_rentals,
        'pending_guest_rentals': pending_guest_rentals,
    }
    
    return render(request, 'core/admin/dashboard.html', context)

@login_required
def admin_rentals(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access rental management.')
        return redirect('core:home')
    
    rentals = Rental.objects.all().order_by('-created_at')
    guest_rentals = GuestRental.objects.all().order_by('-created_at')
    
    # Filter rentals
    status = request.GET.get('status')
    if status:
        rentals = rentals.filter(status=status)
        guest_rentals = guest_rentals.filter(status=status)
    
    context = {
        'rentals': rentals,
        'guest_rentals': guest_rentals,
        'title': 'Manage Rentals'
    }
    
    return render(request, 'core/admin/rentals.html', context)

@login_required
def manage_guest_rental(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to manage guest rentals.')
        return redirect('core:home')
    
    guest_rental = get_object_or_404(GuestRental, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            guest_rental.status = 'confirmed'
            guest_rental.save()
            messages.success(request, f'Guest rental {guest_rental.confirmation_code} has been approved.')
        elif action == 'reject':
            guest_rental.status = 'cancelled'
            guest_rental.save()
            messages.success(request, f'Guest rental {guest_rental.confirmation_code} has been rejected.')
    
    return redirect('core:admin_rentals')

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

def guest_rental_confirmation(request, code):
    guest_rental = get_object_or_404(GuestRental, confirmation_code=code)
    return render(request, 'core/guest_rental_confirmation.html', {
        'rental': guest_rental
    })

def check_guest_rental(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        confirmation_code = request.POST.get('confirmation_code')
        
        try:
            guest_rental = GuestRental.objects.get(
                email=email,
                confirmation_code=confirmation_code
            )
            return redirect('core:guest_rental_confirmation', code=guest_rental.confirmation_code)
        except GuestRental.DoesNotExist:
            messages.error(request, 'No rental found with the provided email and confirmation code.')
    
    return render(request, 'core/check_guest_rental.html')
