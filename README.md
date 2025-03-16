# RentWheels

A modern car rental management system built with Django.

## Features

- 🚗 Vehicle Management
- 👤 User & Guest Accounts
- 📱 Phone Number Authentication
- 🎫 Unique Rental IDs
- 📊 Rental Tracking
- 🔐 Secure Authentication
- 📱 Responsive Design

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rentwheels.git
cd rentwheels
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to access the application.

## Development

See [Development Documentation](docs/development_documentation_v1.1.md) for detailed technical documentation.

### Project Structure
```
rentwheels/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   └── urls.py            # URL routing
├── templates/             # HTML templates
├── static/                # Static files
├── media/                 # User uploads
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Copyright © 2025 RentWheels. All rights reserved.

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/rentwheels
