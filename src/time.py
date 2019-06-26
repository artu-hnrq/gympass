from datetime import timedelta
import re

MINUTES_PER_HOUR =              60
SECONDS_PER_MINUTE =            60
MILLISECONDS_PER_SECOND =       1000
MICROSECONDS_PER_MILLISECOND =  1000
MILLISECONDS_PER_HOUR =         MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE * MINUTES_PER_HOUR

# Duration class was built to simplify time amount management
class Duration(timedelta):

    # It can be instanciated from a string, a dictionary or a timedelta object
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
            raise ValueError(f'{type(args)} is not supported')

    # Diffrent from it's superclass, the Duration is measured in minutes, seconds and milliseconds
    # This property methods help to obtain this values from it's superclass persistence format
    @property
    def minutes(self):          return int(super().seconds / SECONDS_PER_MINUTE)

    @property
    def seconds(self):          return super().seconds % SECONDS_PER_MINUTE

    @property
    def milliseconds(self):     return int(self.microseconds / MICROSECONDS_PER_MILLISECOND)

    # Obtain the total time amount in milliseconds
    def to_milliseconds(self):
        return MILLISECONDS_PER_SECOND * super().seconds + self.milliseconds

    # Overwrite the interation with the + and - operators to result in a Duration object
    def __add__(self, other):
        return Duration(super(Duration, self).__add__(other))

    def __sub__(self, other):
        return Duration(super(Duration, self).__sub__(other))

    # Overwrite the object string output presentation
    def __str__(self):
        return f'{self.minutes}min {self.seconds}s {self.milliseconds}ms'
