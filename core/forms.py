from django import forms
from django.contrib.auth.models import User
from .models import Rental, Review, Vehicle
from django.utils import timezone

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'end_date', 'pickup_location', 'dropoff_location']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('End date must be after start date.')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'make', 'model', 'year', 'license_plate', 
                 'daily_rate', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'daily_rate': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = timezone.now().year
        if year > current_year + 1:
            raise forms.ValidationError(f'Year cannot be greater than {current_year + 1}')
        if year < 1900:
            raise forms.ValidationError('Year cannot be earlier than 1900')
        return year

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get('license_plate')
        if Vehicle.objects.filter(license_plate=license_plate).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This license plate is already registered.')
        return license_plate 