import re
from datetime import timedelta
import util

# time, code, name, num, duration, average

# Posição Chegada
# Código Piloto
# Nome Piloto
# Qtde Voltas Completadas
# Tempo Total de Prova
# Descobrir a melhor volta de cada piloto
# Descobrir a melhor volta da corrida
# Calcular a velocidade média de cada piloto durante toda corrida
# Descobrir quanto tempo cada piloto chegou após o vencedor

# ------------------------------------------

class InputManager:
    separator = re.compile('[ \–\t]+')

    def load(self, archive_name):
        race_log = {}

        with open(archive_name) as log:
            for line in log:
                line = self.separator.split(line)

                driver = (line[1], line[2])             # code, name
                lap = (
                    line[0],                            # time
                    int(line[3]),                       # num
                    util.parse_duration(line[4]),       # duration
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
    race_time = timedelta()
    best_lap = (0, timedelta(1))
    average_speed = 0

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

    @property
    def num_of_laps(self) : return len(self.laps)

# ------------------------------------------
HOUR_MICROSECOND_REASON = 60 * 60 * (10 ** 6)

class Race:
    competitors = []
    best_lap = ((), timedelta(1))
    lap_distance = 0

    def __init__(self, log):
        runners = []

        for driver in log:
            runner = RunnerStatus(driver, log[driver])

            if runner.best_lap[1] < self.best_lap[1]:
                self.best_lap = (driver, runner.best_lap[1])

            runners.append(runner)

        self.competitors = sorted(runners, key = lambda e: e.race_time)

        # race_average
        lap_reference = self.competitors[0].laps[0]
        self.lap_distance = util.to_milliseconds(lap_reference[2]) * (lap_reference[3] / HOUR_MICROSECOND_REASON)

        for driver in self.competitors:
            driver.average_speed = round((self.lap_distance * driver.num_of_laps / util.to_milliseconds(driver.race_time)) * HOUR_MICROSECOND_REASON, 2)

    def __str__(self):
        str = '\n'

        runner_str = '{0}-{1} made {2} laps in {3} [{9}km/h], finishing at {4}{5}. \t\t His best lap was the {6} ({7}){8}.\n'

        for i in range(len(self.competitors)):
            runner = self.competitors[i]

            delay = ''
            if i > 0:
                delay = ' (+{0})'.format(util.to_str(runner.race_time - self.competitors[0].race_time))

            best = ''
            if runner.driver == self.best_lap[0]:
                best = ' that was the best lap of the race'

            str += runner_str.format(
                runner.code,                                # 0. code
                runner.name,                                # 1. name
                len(runner.laps),                           # 2. num of laps
                util.to_str(runner.race_time),              # 3. race time
                util.to_ordinal(i+1),                       # 4. position
                delay,                                      # 5. (delay from the first)
                util.to_ordinal(runner.best_lap[0]),        # 6. best lap number
                util.to_str(runner.best_lap[1]),            # 7. best lap duration
                best,                                       # 8. (best race lap)
                runner.average_speed                        # 9. average
            )

        with open('result', "w") as archive:
            archive.write(str)

        return str

# ------------------------------------------

if __name__ == '__main__':
    im = InputManager()
    race = Race(im.load('race.log'))
    print(race)
