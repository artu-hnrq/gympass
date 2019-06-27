import unittest
from .test_duration import DurationTestCase
from .test_io_maneger import IoManagerTestCase
from .test_race import RaceTestCase
from .test_runner_status import RunnerStatusTestCase

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest([
        DurationTestCase(),
        IoManagerTestCase(),
        RunnerStatusTestCase(),
        RaceTestCase()
    ])
    unittest.TextTestRunner().run(suite)
