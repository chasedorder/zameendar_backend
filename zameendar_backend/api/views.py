import time

from celery import shared_task
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView


@shared_task
def demo_task():
    time.sleep(5)
    print("demo task done")


class RunTask(APIView):
    def get(self, request):
        demo_task.delay()
        return Response("Task add to queue")
