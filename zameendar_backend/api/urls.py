from django.urls import include, path

from .views import RunTask

urlpatterns = [
    path("run_task/", RunTask.as_view()),
]
