import re
from util import *
from main import Race

# ------------------------------------------
IO_PATH = 'io/'

class IoManager:
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

        return Race(race_log);

    def save(self, str):
        with open(IO_PATH + 'result.txt', "w") as archive:
            archive.write(str)
