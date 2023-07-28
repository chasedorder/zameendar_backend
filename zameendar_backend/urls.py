from django.contrib import admin
from django.urls import include, path
from django.urls import re_path as url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("api/", include("zameendar_backend.api.urls")),
    url(r"^", include("django.contrib.auth.urls")),
]
