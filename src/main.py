import re
from datetime import timedelta
import util
from util import Duration

# time, code, name, num, duration, average

# ------------------------------------------
IO_PATH = 'io/'

class InputManager:
    separator = re.compile('[ \–\t]+')

    def load(self, archive_name):
        race_log = {}

        with open(IO_PATH + archive_name) as log:
            for line in log:
                line = self.separator.split(line)

                driver = (line[1], line[2])             # code, name
                lap = (
                    int(line[3]),                       # num
                    Duration(line[4]),                  # duration
                    float(line[5].replace(',', '.'))    # average
                )

                driver_log = race_log.get(driver, [])
                driver_log.append(lap)
                race_log.setdefault(driver, driver_log)

        return race_log;

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
        num, duration, average = laps[0]
        lap_distance = duration.to_total_milliseconds() * (average / HOUR_MICROSECOND_REASON)

        self.average_speed = round((lap_distance * self.num_of_laps / self.race_time.to_total_milliseconds()) * HOUR_MICROSECOND_REASON, 2)

    @property
    def code(self):                 return self.driver[0]

    @property
    def name(self):                 return self.driver[1]

    @property
    def num_of_laps(self):          return len(self.laps)

    @property
    def best_lap_num(self):         return util.to_ordinal(self.best_lap[0])

    @property
    def best_lap_duration(self):    return self.best_lap[1]

# ------------------------------------------
HOUR_MICROSECOND_REASON = 60 * 60 * (10 ** 6)

class Race:
    competitors = []
    best_lap = timedelta(1)
    lap_distance = 0

    def __init__(self, log):
        runners = []

        for driver in log:
            runner = RunnerStatus(driver, log[driver])

            if runner.best_lap_duration < self.best_lap:
                self.best_lap = runner.best_lap_duration

            runners.append(runner)

        self.competitors = sorted(runners, key = lambda r: r.race_time)

    def __str__(self):
        str = '\n'

        runner_str = (
            '{code}-{name} made {num_of_laps} laps in {race_time} [{average_speed}km/h], '
            'finishing at {position}{delay}.'
            '\t His best lap was the {best_lap_num} ({best_lap_duration}){best_race_lap}.\n'
        )

        for i in range(len(self.competitors)):
            runner = self.competitors[i]

            answer = {
                'code':                 runner.code,
                'name':                 runner.name,
                'num_of_laps':          runner.num_of_laps,
                'race_time':            runner.race_time,
                'position':             util.to_ordinal(i+1),
                'delay':                f' (+{runner.race_time - self.winner.race_time})' if i>0 else '',
                'average_speed':        runner.average_speed,
                'best_lap_num':         runner.best_lap_num,
                'best_lap_duration':    runner.best_lap_duration,
                'best_race_lap':        ' that was the best lap of the race'
                                        if runner.best_lap_duration == self.best_lap else ''
            }

            str += runner_str.format(**answer)

        with open(IO_PATH + 'result.txt', "w") as archive:
            archive.write(str)

        return str

    @property
    def winner(self): return self.competitors[0]

# ------------------------------------------

if __name__ == '__main__':
    im = InputManager()
    race = Race(im.load('race.log'))
    print(race)
