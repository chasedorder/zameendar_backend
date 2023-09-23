import json


def json_to_python(data):
    if data:
        return json.loads(data)
    else:
        return None
