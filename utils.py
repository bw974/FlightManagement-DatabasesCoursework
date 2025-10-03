def validate_datetime(dt_str):
    """Ensure datetime is in format YYYY-MM-DD HH:MM"""
    try:
        datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
    
def validate_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def get_connection(db_name):
    return sqlite3.connect(db_name)