import math
import random
import urllib.parse
import urllib.request


def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode(
        {"apikey": apikey, "numbers": numbers, "message": message, "sender": sender}
    )
    data = data.encode("utf-8")
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


def generate_six_digit_otp():
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    return otp
