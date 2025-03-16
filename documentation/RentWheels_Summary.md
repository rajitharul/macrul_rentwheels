# RentWheels - Car Rental Management System

## Overview
RentWheels is a comprehensive car rental management system built with Django that provides both customer-facing features and administrative capabilities. The application allows users to browse, book, and manage vehicle rentals while providing administrators with tools to manage the fleet and rental operations.

## Key Features

### Public Features
1. **Homepage**
   - Dynamic carousel showcase with three featured images
   - Featured vehicles section
   - "Why Choose Us" section highlighting key benefits
   - "How It Works" section explaining the rental process
   - Call-to-action section for user engagement

2. **Vehicle Management**
   - Browse available vehicles
   - Filter vehicles by:
     - Type
     - Price range
     - Availability
   - Search functionality
   - Detailed vehicle information pages
   - Vehicle images and specifications

3. **Rental System**
   - Online booking system
   - Date selection for rental period
   - Rental history for users
   - Booking confirmation system
   - View rental details and status

4. **User Authentication**
   - User registration
   - Login/Logout functionality
   - Profile management
   - Password reset capabilities
   - Email verification

### Administrative Features
1. **Django Admin Interface** (`/admin/`)
   - User management
   - Vehicle inventory management
   - Rental management
   - System configuration

2. **Custom Management Dashboard** (`/management/dashboard/`)
   - Overview of rental operations
   - Quick access to key metrics
   - Recent activity monitoring
   - System status updates

3. **Vehicle Management**
   - Add new vehicles
   - Edit vehicle details
   - Toggle vehicle availability
   - Manage vehicle images
   - Track vehicle status

4. **Rental Management**
   - View all rentals
   - Process rental requests
   - Track rental status
   - Manage rental returns
   - Generate rental reports

## Technical Details

### URL Structure
1. **Public URLs**
   - Home: `/`
   - Vehicles: `/vehicles/`
   - Vehicle Detail: `/vehicles/<id>/`
   - Rentals: `/rentals/`
   - User Profile: `/profile/`

2. **Administrative URLs**
   - Django Admin: `/admin/`
   - Management Dashboard: `/management/dashboard/`
   - Vehicle Management: `/management/vehicles/`
   - Rental Management: `/management/rentals/`

### User Roles
1. **Public Users**
   - Browse vehicles
   - View vehicle details
   - Register/Login

2. **Authenticated Users**
   - Book vehicles
   - Manage bookings
   - View rental history
   - Update profile

3. **Staff Users**
   - Access management dashboard
   - Manage vehicles
   - Process rentals
   - Generate reports

4. **Superusers**
   - Full system access
   - User management
   - System configuration
   - Database management

## Design Features
1. **Responsive Design**
   - Mobile-friendly interface
   - Adaptive layouts
   - Touch-friendly controls
   - Responsive images

2. **UI Components**
   - Bootstrap framework
   - Custom carousel
   - Card-based layouts
   - Interactive forms
   - Modal dialogs
   - Toast notifications

3. **Visual Elements**
   - Hero section with dynamic slider
   - Icon-based feature highlights
   - Progress indicators
   - Status badges
   - Action buttons

## Security Features
1. **Authentication**
   - Secure password handling
   - Email verification
   - Password reset functionality
   - Session management

2. **Authorization**
   - Role-based access control
   - Permission management
   - Secure views
   - Protected admin routes

## Data Management
1. **Vehicle Information**
   - Make and model
   - Year
   - Type/Category
   - Daily rate
   - Availability status
   - Images

2. **Rental Records**
   - Customer details
   - Rental period
   - Payment information
   - Status tracking
   - Return details

3. **User Data**
   - Personal information
   - Contact details
   - Rental history
   - Preferences

## Future Enhancements
1. **Planned Features**
   - Payment gateway integration
   - SMS notifications
   - Mobile app development
   - Advanced reporting
   - Customer reviews system

2. **Potential Improvements**
   - Multi-language support
   - Advanced booking features
   - Loyalty program
   - API development
   - Integration with external systems

## Getting Started
1. **Requirements**
   - Python 3.x
   - Django 5.x
   - Virtual environment
   - Required packages (see requirements.txt)

2. **Installation**
   - Clone repository
   - Create virtual environment
   - Install dependencies
   - Configure settings
   - Run migrations
   - Create superuser
   - Start development server

## Maintenance
1. **Regular Tasks**
   - Database backups
   - System updates
   - Security patches
   - Performance monitoring
   - User support

2. **Troubleshooting**
   - Check error logs
   - Monitor system resources
   - Review user feedback
   - Test functionality
   - Update documentation

---

*Last Updated: March 16, 2025*
*Version: 1.0* 