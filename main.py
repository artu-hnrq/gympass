import re
from datetime import timedelta
import util

# time, code, name, num, duration, average
"""
Posição Chegada
# Código Piloto
# Nome Piloto
#. Qtde Voltas Completadas
# Tempo Total de Prova
# Descobrir a melhor volta de cada piloto
# Descobrir a melhor volta da corrida
Calcular a velocidade média de cada piloto durante toda corrida
Descobrir quanto tempo cada piloto chegou após o vencedor
"""

# ------------------------------------------

class InputManager:
    separator = re.compile('[ \–\t]+')

    def load(self, archive_name):
        race_log = {}

        with open(archive_name) as log:
            for line in log:
                line = self.separator.split(line)

                driver = (line[1], line[2])
                lap = (
                    line[0],
                    int(line[3]),
                    util.parse_duration(line[4]),
                    float(line[5].replace(',', '.'))
                )

                driver_log = race_log.get(driver, [])
                driver_log.append(lap)
                race_log.setdefault(driver, driver_log)

        return race_log;

# ------------------------------------------
class RunnerStatus:
    driver = ()
    laps = []
    race_time = timedelta(0)
    best_lap = (0, timedelta(1))

    def __init__(self, driver, laps):
        self.driver = driver
        self.laps = laps

        for lap in laps:
            time, num, duration, average = lap
            self.race_time += duration

            if duration < self.best_lap[1]:
                self.best_lap = (num, duration)

    @property
    def code(self): return self.driver[0]

    @property
    def name(self): return self.driver[1]

    def __str__(self):
        # 0. code
        # 1. name
        # 2. num of laps
        # 3. race time
        # 4. position
        # 5. (delay from the first)
        # 6. best lap number
        # 7. best lap duration
        # 8. (best race lap)
        return """{0}-{1} made {2} laps in {3}m, finishing in {4} {5}.
        His best lap was the {6} ({7}m){8}\n"""


# ------------------------------------------
class Race:
    competitors = []
    race_best_lap = ((), timedelta(1))

    def __init__(self, log):
        runners = []

        for driver in log:
            runner = RunnerStatus(driver, log[driver])

            if runner.best_lap[1] < self.race_best_lap[1]:
                self.race_best_lap = (driver, runner.best_lap[1])

            runners.append(runner)

        self.competitors = sorted(runners, key = lambda e: e.race_time)

    def __str__(self):
        str = ''
        for i in range(len(self.competitors)):
            runner = self.competitors[i]

            delay = ''
            if i > 0:
                delay = '(+{0})'.format(runner.race_time - self.competitors[0].race_time)

            best = '.'
            if runner.driver == self.race_best_lap[0]:
                best = ' that was the best lap of the race.'

            str += runner.__str__().format(runner.code, runner.name, len(runner.laps), runner.race_time, i+1, delay, runner.best_lap[0], runner.best_lap[1], best)

        return str

# ------------------------------------------

if __name__ == '__main__':
    im = InputManager()
    race = Race(im.load('race.log'))
    print(race)
