from datetime import datetime


def now():
    """Returns the current date and time with timezone information."""
    return datetime.now().astimezone()
