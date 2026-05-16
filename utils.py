import time


def format_time(seconds):

    hours = int(seconds // 3600)

    seconds %= 3600

    minutes = int(seconds // 60)

    seconds %= 60

    return f"{hours}h {minutes}m {int(seconds)}s"


def now():

    return int(time.time())
