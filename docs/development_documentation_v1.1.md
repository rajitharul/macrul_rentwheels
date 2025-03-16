# RentWheels Development Documentation v1.1

## System Overview
RentWheels is a modern car rental management system built with Django. It provides a comprehensive platform for managing vehicle rentals, user accounts, and rental tracking.

## Technical Stack
- **Backend**: Django 4.x
- **Frontend**: Bootstrap 5.3
- **Database**: SQLite (Development)
- **Authentication**: Django Authentication System
- **Forms**: Django Crispy Forms

## Core Features

### 1. Vehicle Management
- Vehicle listing with detailed information
- Vehicle availability tracking
- Vehicle type categorization (sedan, SUV, sports, luxury, van)
- Image upload support
- Dynamic pricing based on vehicle type

#### Key Models
```python
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vehicle_type = models.CharField(choices=VEHICLE_TYPES)
    daily_rate = models.DecimalField()
    is_available = models.BooleanField()
```

### 2. User System
- Regular user accounts
- Guest rental accounts
- Phone number-based authentication
- Profile management
- Role-based access control

#### Authentication Flow
1. Regular users: Email/password login
2. Guest users: Phone number + password
3. Admin users: Superuser access

### 3. Rental System
- Unique rental ID generation
- Multiple rental statuses (pending, approved, completed, cancelled)
- Date-based availability checking
- Location tracking (pickup/dropoff)

#### Rental Model
```python
class Rental(models.Model):
    rental_id = models.CharField(unique=True)
    customer = models.ForeignKey(User)
    vehicle = models.ForeignKey(Vehicle)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 4. Guest Rental System
- Quick rental without full registration
- Automatic account creation
- Rental tracking via rental ID
- Simplified form with essential fields

#### Guest Rental Form
```python
class GuestRentalForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField(validators=[phone_regex])
    password = forms.CharField(widget=forms.PasswordInput)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
```

## URL Structure

### Public URLs
- `/` - Home page
- `/vehicles/` - Vehicle listing
- `/vehicles/<id>/` - Vehicle details
- `/account/login/` - User login
- `/account/signup/` - User registration

### Authenticated URLs
- `/profile/` - User profile
- `/rentals/` - User's rentals
- `/rentals/<id>/` - Rental details
- `/profile/edit/` - Edit profile

### Admin URLs
- `/admin/` - Django admin
- `/management/dashboard/` - Admin dashboard
- `/management/rentals/` - Rental management
- `/management/vehicles/` - Vehicle management

## Key Components

### 1. Views
- Class-based views for CRUD operations
- Function-based views for complex logic
- Decorator-based access control

### 2. Forms
- Django forms with crispy-forms styling
- Custom form validation
- AJAX-enabled forms where needed

### 3. Templates
- Base template with Bootstrap 5
- Modular template structure
- Responsive design

### 4. Static Files
```
static/
├── css/
│   └── style.css
├── js/
│   └── main.js
└── img/
    └── vehicles/
```

## Security Features

### 1. Authentication
- Password hashing
- Session management
- CSRF protection
- Phone number validation

### 2. Authorization
- Permission-based access
- Role-based views
- Secure form handling

### 3. Data Validation
- Form validation
- Model validation
- Date range validation
- Unique constraint checks

## Database Schema

### Core Tables
1. **Users**
   - Default Django User model
   - Extended profile information

2. **Vehicles**
   - Vehicle information
   - Availability status
   - Pricing details

3. **Rentals**
   - Rental records
   - Status tracking
   - Customer information

## API Endpoints (Future)

### Planned REST API
```
/api/v1/
├── vehicles/
├── rentals/
└── users/
```

## Development Guidelines

### 1. Code Style
- Follow PEP 8
- Use Django coding style
- Document all functions
- Type hints where possible

### 2. Git Workflow
- Feature branches
- Pull request reviews
- Semantic versioning
- Conventional commits

### 3. Testing
- Unit tests for models
- Integration tests for views
- Form validation tests
- Security tests

## Deployment

### Requirements
- Python 3.8+
- Django 4.x
- PostgreSQL (Production)
- Redis (Optional)

### Environment Variables
```
DEBUG=True/False
SECRET_KEY=your-secret-key
DATABASE_URL=your-db-url
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Future Enhancements

### Version 1.2 (Planned)
- Payment integration
- Email notifications
- SMS notifications
- API endpoints
- Advanced search
- Analytics dashboard

## Known Issues
1. Success message display in some forms
2. Date picker timezone handling
3. Image upload size limitations

## Support
For technical support or bug reports:
- Create an issue in the repository
- Contact the development team

## License
Copyright © 2025 RentWheels. All rights reserved.
