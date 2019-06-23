from datetime import *
import re

class Duration(timedelta):
    def __new__(cls, args = '0'):
        if isinstance(args, str):
            regex = re.compile(
                r'(?P<minutes>\d+?)'             #
                r'(\:(?P<seconds>\d+?))?'        #
                r'(\.(?P<milliseconds>\d+?))?$'  #
            )
            parts = regex.match(args).groupdict().items()
            args = {
                unit:int(value)
                for (unit, value)
                in parts
                if value != None
            }
            return super(Duration, cls).__new__(cls, **args)

        elif isinstance(args, dict):
            return super(Duration, cls).__new__(cls, **args)

        elif isinstance(args, timedelta):
            return Duration(f'0:{args.seconds}.{int(args.microseconds / 1000)}')

        else:
            raise ValueError(type(args))

    @property
    def min(self): return int(self.seconds / 60)

    @property
    def s(self): return self.seconds - (self.min * 60)

    @property
    def ms(self): return int(self.microseconds / (10 ** 3))

    def to_total_milliseconds(self):
        return self.seconds * 1000 + self.ms

    def __add__(self, other):
        return Duration(super().__add__(other))

    def __sub__(self, other):
        return Duration(super().__sub__(other))

    def __str__(self):
        return f'{self.min}min {self.s}s {self.ms}ms'

def to_ordinal(position):
    map = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fifth',
        6: 'sixth',
        7: 'seventh',
        8: 'eighth',
        9: 'nineth'
    }
    return map[position]
