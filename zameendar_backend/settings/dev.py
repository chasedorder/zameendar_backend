from .base import *

ALLOWED_HOSTS = [".ngrok-free.app", "127.0.0.1", "192.168.44.128"]

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

# AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")

CELERY_BROKER_URL = env("CELERY_BROKER_URL")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CSRF_TRUSTED_ORIGINS = ["https://98d3-180-188-232-110.ngrok-free.app", "http://127.0.0.1"]

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "media")
