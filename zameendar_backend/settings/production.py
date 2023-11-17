from .base import *

ALLOWED_HOSTS = [
    "64.227.177.77",
    "127.0.0.1",
    "192.168.44.128",
    "zameendarproperties.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

CSRF_TRUSTED_ORIGINS = ["https://64.227.177.77", "http://127.0.0.1"]

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "media")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "your_username@gmail.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
