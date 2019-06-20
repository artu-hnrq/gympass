from datetime import *
import re

def parse_duration(duration_str):
    regex = re.compile(r'(?P<minutes>\d+?)\:(?P<seconds>\d+?)\.(?P<microseconds>\d+?)$')

    parts = regex.match(duration_str).groupdict().items()

    params = {
        unit:int(value)
        for (unit, value)
        in parts
    }

    return timedelta(**params)
