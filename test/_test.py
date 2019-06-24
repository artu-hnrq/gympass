import unittest
from datetime import timedelta
import os

from .. import src

# ------------------------------------------

class UtilTest(unittest.TestCase):
    def test(self):
        t = timedelta(minutes=4, seconds=23, milliseconds=233)
        print(t)
        self.assertEqual(t, parse_duration("4:23.233"))

# ------------------------------------------

class AnyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(44.275, float("44,275".replace(',', '.')))
        self.assertEqual(1001, to_milliseconds(timedelta(seconds=1, milliseconds=1)))

# ------------------------------------------

class InputManagerTest(unittest.TestCase):
    archive_name = 'InputManager.test'
    content = "23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275"

    def test(self):
        archive_name = self.archive_name
        with open(IO_PATH + archive_name, "w") as archive:
            archive.write(self.content)

        im = InputManager()
        input = im.load(archive_name)

        self.assertEqual(1, len(input))

        if os.path.exists(IO_PATH + archive_name):
            os.remove(IO_PATH + archive_name)

# ------------------------------------------

if __name__ == '__main__':
    unittest.main()
