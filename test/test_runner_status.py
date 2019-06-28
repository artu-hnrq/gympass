from unittest import TestCase

from .util import *
from .data_fabric import *
from src.runner_status import *

# ------------------------------------------
class RunnerStatusTestCase(TestCase):
    driver = None
    laps = None

    lap_distance = 10

    def setUp(self):
        self.driver = createDriver()
        self.laps = createLaps(self.lap_distance)

    # Try to create a RunnerStatus instance with some non-supported argument types
    @expectError(TypeError)
    def test_UnsupportedArgument_1(self):
        RunnerStatus(1,2)

    @expectError(TypeError)
    def test_UnsupportedArgument_2(self):
        RunnerStatus({}, [23.1, (True, 'a')])

    # Verify all class atributes construction results
    def test(self):
        runner = RunnerStatus(self.driver, self.laps)

        num_of_laps = len(self.laps)

        best_lap = [
            (num, lap_duration)
            for (num, lap_duration, average_speed)
            in self.laps
            if lap_duration == min([lap[1] for lap in self.laps])
        ][0]

        race_time = Duration()
        for lap in self.laps:
            race_time += lap[1]

        average_speed = round(self.lap_distance * num_of_laps / race_time.to_milliseconds() * MILLISECONDS_PER_HOUR, 2)

        assertEquals = [
            (self.driver[0], runner.code),
            (self.driver[1], runner.name),

            (num_of_laps, runner.num_of_laps),
            (best_lap[0], runner.best_lap_num),
            (best_lap[1], runner.best_lap_duration),

            (race_time, runner.race_time),
            (average_speed, runner.average_speed)
        ]

        for equivalence in assertEquals:
            self.assertEqual(equivalence[0], equivalence[1])
