from unittest import TestCase
import random

from .util import *
from .data_fabric import *
from src.race import *
from src.time import *

# ------------------------------------------
class RaceTestCase(TestCase):
    lap_distance = 10
    race_log = {}

    def setUp(self):
        for i in range(random.randint(3, 5)):
            self.race_log[createDriver()] = createLaps(self.lap_distance)

    # Try to create a Race instance with some non-supported types
    @expectError(TypeError)
    def test_UnknowedType_1(self):
        Race(1)

    @expectError(TypeError)
    def test_UnknowedType_2(self):
        Race((True))

    @expectError(TypeError)
    def test_UnknowedType_3(self):
        Race([4.5])

    # Try to get the winner from a Race without competitors
    @expectError(IndexError)
    def test_ZeroCompetitors(self):
        Race({}).winner

    # Verify the order of the competitors result
    def test_positions(self):
        race = Race(self.race_log)

        positions = []
        for driver in self.race_log:
            race_time = Duration('0')

            laps = self.race_log[driver]
            for lap in laps:
                race_time += lap[1]

            positions.append((driver, len(laps), race_time))

        positions = [
            driver
            for (driver, num_of_laps, race_time)
            in sorted(positions,
                key = lambda each: each[2] + timedelta(hours = 4 - each[1])
            )
        ]

        for i in range(len(positions)):
            self.assertEqual(positions[i], race.competitors[i].driver)
        self.assertEqual(positions[0], race.winner.driver)

    # Verify correct calculation of the race's best lap
    def test_best_lap(self):
        race = Race(self.race_log)

        best_lap = Duration('60')

        for driver in self.race_log:

            laps = self.race_log[driver]
            for lap in laps:
                if lap[1] < best_lap:
                    best_lap = lap[1]

        self.assertEqual(best_lap, race.best_lap)
