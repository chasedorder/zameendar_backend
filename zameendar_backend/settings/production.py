from .base import *

ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "djangoapplikututorial",
        "USER": "USERNAME",  # Replace with your actual database username
        "PASSWORD": "PASSWORD",  # Replace with your actual database password
        "HOST": "END_POINT",  # Replace with your actual database endpoint
        "PORT": "5432",  # Replace with your actual database port
    }
}
