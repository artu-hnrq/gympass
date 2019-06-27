from unittest import TestCase

from src.race import *

# ------------------------------------------
class RunnerStatusTestCase(TestCase):
    def test(self):
        runner = RunnerStatus(('0', 'Artú'), [
            (1, Duration('1'), 100.0),
            (2, Duration('4:00.005'), 25.0),
            (3, Duration('2:05'), 50.0)
        ])

        assertEquals = [
            ('0', runner.code),
            ('Artú', runner.name),

            (3, runner.num_of_laps),
            ('first', runner.best_lap_num),
            (Duration('1'), runner.best_lap_duration),

            (Duration('7:05.005'), runner.race_time),
            (42.35, runner.average_speed)
        ]

        for equivalence in assertEquals:
            self.assertEqual(equivalence[0], equivalence[1])
