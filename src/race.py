from . import util
from .runner_status import *

# ------------------------------------------
class Race:
    competitors = []
    best_lap = timedelta(1)

    def __init__(self, log):
        runners = []

        for driver in log:
            runner = RunnerStatus(driver, log[driver])

            if runner.best_lap_duration < self.best_lap:
                self.best_lap = runner.best_lap_duration

            runners.append(runner)

        # Ordenating runners by position
        def ordenate(runner):
            # increase the return from their that didn't finish the race
            return runner.race_time + timedelta(hours = 4 - runner.num_of_laps)

        self.competitors = sorted(runners, key = ordenate)


    def __str__(self):
        str = '\n'

        runner_str = (
            '{code}-{name} made {num_of_laps} laps in {race_time} [{average_speed}km/h], '
            'finishing at {position}{delay}.'
            '\t His best lap was the {best_lap_num} ({best_lap_duration}){best_race_lap}.\n'
        )

        for i in range(len(self.competitors)):
            runner = self.competitors[i]

            str += runner_str.format(**{
                'code':                 runner.code,
                'name':                 runner.name,
                'num_of_laps':          runner.num_of_laps,
                'race_time':            runner.race_time,
                'position':             util.to_ordinal(i+1),
                'delay':                f' (+{runner.race_time - self.winner.race_time})' if i>0 else '',
                'average_speed':        runner.average_speed,
                'best_lap_num':         util.to_ordinal(runner.best_lap_num),
                'best_lap_duration':    runner.best_lap_duration,
                'best_race_lap':        ' that was the best lap of the race'
                                        if runner.best_lap_duration == self.best_lap else ''
            })

        return str

    @property
    def winner(self): return self.competitors[0]
