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

def to_str(duration):
    m = int(duration.seconds / 60)
    s = duration.seconds - (m * 60)
    ms = duration.microseconds

    return '{0}m {1}s {2}ms'.format(m, s, ms)

def to_microseconds(duration):
    return duration.microseconds + duration.seconds * (10 ** 6)

def to_ordinal(position):
    map = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fiveth',
        6: 'sixth',
        7: 'seventh',
        8: 'eighth',
        9: 'nineth'
    }
    return map[position]
