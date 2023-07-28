from datetime import datetime, timedelta


def formatting_date(date_time):
    if date_time is None:
        return None
    return date_time.strftime("%d/%m/%Y")


def formatting_time(date_time):
    if date_time is None:
        return None
    return date_time.strftime("%H:%M %p")


def formatting_date_time(date_time):
    if date_time is None:
        return None
    return date_time.strftime("%d/%m/%Y %H:%M:%S %p")


def convert_string_to_date(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, "%d/%m/%Y")


def convert_string_to_time(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, "%H:%M:%S %p")


def convert_string_to_datetime(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, "%d/%m/%Y %H:%M:%S %p")


def get_days_ago_date(days):
    if days is None:
        return None
    return datetime.now() - timedelta(days=days)
