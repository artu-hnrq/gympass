from .time import *

# ------------------------------------------
class RunnerStatus:
    driver = ()
    laps = []
    race_time = Duration()
    best_lap = (0, timedelta(1))
    average_speed = 0

    def __init__(self, driver, laps):
        self.driver = driver
        self.laps = laps

        for lap in laps:
            num, duration, average = lap
            self.race_time += duration

            if duration < self.best_lap[1]:
                self.best_lap = (num, duration)

        # race_average
        num, lap_time, average = laps[0]
        lap_distance = lap_time.to_milliseconds() * (average / MILLISECONDS_PER_HOUR)

        self.average_speed = round((lap_distance * self.num_of_laps / self.race_time.to_milliseconds()) * MILLISECONDS_PER_HOUR, 2)

    @property
    def code(self):                 return self.driver[0]

    @property
    def name(self):                 return self.driver[1]

    @property
    def num_of_laps(self):          return len(self.laps)

    @property
    def best_lap_num(self):         return self.best_lap[0]

    @property
    def best_lap_duration(self):    return self.best_lap[1]
