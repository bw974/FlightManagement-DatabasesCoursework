from datetime import datetime


def validate_datetime(datetime_string: str) -> bool:
    # Ensure datetime is in format YYYY-MM-DD HH:MM
    try:
        datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def validate_int(value: any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def validate_nonempty_string(value: str) -> bool:
    return bool(value and value.strip())
