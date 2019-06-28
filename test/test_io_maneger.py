# -*- coding: utf-8 -*-
import os
from unittest import TestCase
from .util import *

from src.io_manager import *

# Define a decorator that creates an archive in the folder io
# and load it's content before run the test, deleting it at the end
def withInputFile(content):
    archive_name = 'Input.test'

    def decorator(test):
        def do(self):
            with open(IO_PATH + archive_name, "w") as archive:
                archive.write(content)

            io = IoManager()
            input = io.load(archive_name)

            test(self, input)

            if os.path.exists(IO_PATH + archive_name):
                os.remove(IO_PATH + archive_name)

        return do
    return decorator

# ------------------------------------------
class IoManagerTestCase(TestCase):

    # Try to load an inexistent archive
    @expectError(FileNotFoundError)
    def test_FileNotFound(self):
        io = IoManager()
        input = io.load('archive_name')

    # Try to load an archive with unreadable information
    @expectError(ValueError, lambda: os.remove(IO_PATH + 'Input.test'))
    @withInputFile((
        "20:01.002   000 – ARTU   1   S:02.003    4,05\n"
        "  000 – ARTU    8   1   1:02.003    4,05\n"
    ))
    def test_UnknowedFormat(self, input):
        pass

    # Verify the structure built from a valid input
    @withInputFile((
        "20:01.002   100 – ARTU   1   1:02.003    4,05\n"
        "20:01.002   100 – ARTU  2   1:02.003    4,05\n"
        "20:01.002   001 – ARTHUR   1   1:02.003    4,05\n"
        "20:01.002   010 – HENRIQUE   1   1:02.003    4,05\n"
        "20:01.002   001 – ARTHUR   2   1:02.003    4,05\n"
    ))
    def test_StructureLoaded(self, input):
        self.assertEqual(3, len(input))     # Check for 3 drivers

        for driver in [('100', 'ARTU'), ('001', 'ARTHUR'), ('010', 'HENRIQUE')]:
            self.assertTrue(driver in input)         # Check for the mentioned drivers

            laps = input[driver]
            self.assertEqual(len(laps), laps[-1][0])    # Check the number of laps for each driver

            for lap in laps:
                self.assertTrue(isinstance(lap[0], int))
                self.assertTrue(isinstance(lap[1], Duration))
                self.assertTrue(isinstance(lap[2], float))
