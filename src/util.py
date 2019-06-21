from datetime import *
import re

def parse_duration(duration_str):
    regex = re.compile(r'(?P<minutes>\d+?)\:(?P<seconds>\d+?)\.(?P<milliseconds>\d+?)$')
    parts = regex.match(duration_str).groupdict().items()
    params = {
        unit:int(value)
        for (unit, value)
        in parts
    }

    return timedelta(**params)

def to_str(duration):
    min = int(duration.seconds / 60)
    s = duration.seconds - (min * 60)
    ms = int(duration.microseconds / (10 ** 3))

    return '{0}min {1}s {2}ms'.format(min, s, ms)

def to_milliseconds(duration):
    return (duration.microseconds / (10 ** 3)) + (duration.seconds * (10 ** 3))

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
