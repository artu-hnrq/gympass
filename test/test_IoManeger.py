# -*- coding: utf-8 -*-
import os

from .my_testcase import *
from src.in_out import *

# ------------------------------------------
class IoManagerTestCase(MyTestCase):

    # Creates an archive in the folder io before run the test and delete it at the end
    def withInputFile(self, archive_name, content, test):
        with open(IO_PATH + archive_name, "w") as archive:
            archive.write(content)

        test()

        if os.path.exists(IO_PATH + archive_name):
            os.remove(IO_PATH + archive_name)

    # Try to load an inexistent archive
    def test_FileNotFound(self):
        def _1():
            io = IoManager()
            input = io.load('archive_name')

        self.expectError(FileNotFoundError, _1)

    # Try to load an archive with unreadable information
    def test_UnknowedFormat(self):
        archive_name = 'Input.test'
        content = (
            "20:01.002   000 – ARTU   1   S:02.003    4,05\n"
            "  000 – ARTU    8   1   1:02.003    4,05\n"
        )

        def _withImputFile():
            def _expectError():
                io = IoManager()
                input = io.load('archive_name')

            self.expectError(FileNotFoundError, _expectError)

        self.withInputFile(archive_name, content, _withImputFile)

    # Verufy the structure built from a valid input
    def test_StructureLoaded(self):
        archive_name = 'Input.test'
        content = (
            "20:01.002   100 – ARTU   1   1:02.003    4,05\n"
            "20:01.002   100 – ARTU  2   1:02.003    4,05\n"
            "20:01.002   001 – ARTHUR   1   1:02.003    4,05\n"
            "20:01.002   010 – HENRIQUE   1   1:02.003    4,05\n"
            "20:01.002   001 – ARTHUR   2   1:02.003    4,05\n"
        )

        def do():
            im = IoManager()
            input = im.load(archive_name)

            self.assertEqual(3, len(input))                     # Check for 3 drivers

            for driver in [('100', 'ARTU'), ('001', 'ARTHUR'), ('010', 'HENRIQUE')]:
                if driver not in input:
                    self.fail(f'Driver {driver} identification fail')
                else:
                    laps = input[driver]
                    self.assertEqual(len(laps), laps[-1][0])        # Check the number of laps for each driver

        self.withInputFile(archive_name, content, do)
