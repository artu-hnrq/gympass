from datetime import timedelta
import re

MINUTES_PER_HOUR =              60
SECONDS_PER_MINUTE =            60
MILLISECONDS_PER_SECOND =       1000
MICROSECONDS_PER_MILLISECOND =  1000
MILLISECONDS_PER_HOUR =         MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE * MINUTES_PER_HOUR

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
            seconds = args.seconds
            milliseconds = int(args.microseconds / MICROSECONDS_PER_MILLISECOND)

            return Duration(f'0:{seconds}.{milliseconds}')

        else:
            raise ValueError(type(args))

    @property
    def minutes(self):          return int(super(Duration, self).seconds / SECONDS_PER_MINUTE)

    @property
    def seconds(self):          return super(Duration, self).seconds % SECONDS_PER_MINUTE

    @property
    def milliseconds(self):     return int(self.microseconds / MICROSECONDS_PER_MILLISECOND)

    def to_milliseconds(self):
        return MILLISECONDS_PER_SECOND * super().seconds + self.milliseconds

    def __add__(self, other):
        return Duration(super(Duration, self).__add__(other))

    def __sub__(self, other):
        return Duration(super(Duration, self).__sub__(other))

    def __str__(self):
        return f'{self.minutes}min {self.seconds}s {self.milliseconds}ms'


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
