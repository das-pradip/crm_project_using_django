import os
from django.contrib.auth import get_user_model

User = get_user_model()

print("Running createsuperuser script...")

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

print("Username:", username)
print("Email:", email)

if not username or not password:
    print("ENV variables missing")
else:
    if User.objects.filter(username=username).exists():
        print("Superuser already exists")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser CREATED successfully")

