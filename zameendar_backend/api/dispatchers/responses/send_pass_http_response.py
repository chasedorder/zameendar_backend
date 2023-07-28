import json

from django.shortcuts import HttpResponse


def send_pass_http_response(args=None):
    if not args:
        args = {}

    args["status"] = "PASS"

    the_data = json.dumps(args)
    response = HttpResponse(the_data, content_type="application/json")

    return response
