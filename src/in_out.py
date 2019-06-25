# -*- coding: utf-8 -*-
import re
import sys
from .util import *

# ------------------------------------------
IO_PATH = 'io/'

class IoManager:
    separator = re.compile('[ \–\t]+')

    def load(self, archive_name):
        race_log = {}

        try:
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
        except FileNotFoundError:
            raise FileNotFoundError(f"To run this program place the input content in '{IO_PATH + archive_name}'")
        except (AttributeError, ValueError):
            raise ValueError("Certify that the input contet is in the format: '{time} {code} – {name} {lap_num} {lap_duration} {average_speed}'")

        return race_log;

    def save(self, str):
        with open(IO_PATH + 'result.txt', "w") as archive:
            archive.write(str)
