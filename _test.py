import unittest
from datetime import timedelta
import os

from util import *
from main import *

# ------------------------------------------

class UtilTest(unittest.TestCase):
    def test(self):
        self.assertEqual(parse_duration("4:23.233"), timedelta(minutes=4, seconds=23, microseconds=233))

# ------------------------------------------

class AnyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(44.275, float("44,275".replace(',', '.')))
        a, b = (2, 3)
        self.assertEqual(2, a)

# ------------------------------------------

class InputManagerTest(unittest.TestCase):
    archive_name = 'InputManager.test'
    content = "23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275"

    def test(self):
        archive_name = self.archive_name
        with open(archive_name, "w") as archive:
            archive.write(self.content)

        im = InputManager()
        input = im.load(archive_name)

        self.assertEqual(1, len(input))

        if os.path.exists(archive_name):
            os.remove(archive_name)

# ------------------------------------------

if __name__ == '__main__':
    unittest.main()
