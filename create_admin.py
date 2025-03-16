import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentwheels.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@rentwheels.com'
password = 'admin123'

try:
    superuser = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f'Superuser "{username}" was created successfully!')
except Exception as e:
    print(f'Error creating superuser: {str(e)}')
