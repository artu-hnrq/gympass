# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from src.util import *
from .my_testcase import *

# ------------------------------------------
class DurationTestCase(MyTestCase):
    map = [
        (timedelta(), '0:00.000', '0min 0s 0ms', 0),
        (
            timedelta(minutes=10),                                      # Equivalent timedelta object
            '10:00.000',                                                # Equivalent Diration input string
            '10min 0s 0ms',                                             # Equivalent Duration output string
            10 * SECONDS_PER_MINUTE * MILLISECONDS_PER_SECOND           # total of milliseconds
        ),
        (
            timedelta(minutes=9, seconds=8),
            '9:08',
            '9min 8s 0ms',
            (9 * SECONDS_PER_MINUTE + 8) * MILLISECONDS_PER_SECOND
        ),
        (
            timedelta(minutes=1, seconds=2, milliseconds=3),
            '1:02.003',
            '1min 2s 3ms',
            (1 * SECONDS_PER_MINUTE + 2) * MILLISECONDS_PER_SECOND + 3
        ),
        (
            timedelta(seconds=62, milliseconds=3),
            '1:02.003',
            '1min 2s 3ms',
            (1 * SECONDS_PER_MINUTE + 2) * MILLISECONDS_PER_SECOND + 3
        )
    ]

    # Try to create a Duration instance with some not-supported types
    def test_UnknowedType(self):
        def _1():
            Duration(1)

        def _2():
            Duration(['0:00.001'])

        def _3():
            Duration(True)

        self.expectError(ValueError, _1)
        self.expectError(ValueError, _2)
        self.expectError(ValueError, _3)

    # Try to create a Duration instance with some not-supported arguments
    def test_WrongArgument(self):
        def _1():
            Duration("error")

        def _2():
            Duration({'minutes': 3, 'unknowedUnit': 3})

        def _3():
            Duration({'hours': [True]})

        self.expectError(AttributeError, _1)
        self.expectError(TypeError, _2)
        self.expectError(TypeError, _3)

    # Verify the equivalence between an timedelta object and the Duration created by a string
    def test_Parse(self):
        for each in self.map:
            self.assertEqual(each[0], Duration(each[1]))

    # Verify the equivalence between an timedelta object and the Duration created by it
    def test_create(self):
        t = timedelta(hours=1)
        self.assertEqual(t, Duration(t))

        t = timedelta(days=2)
        self.assertNotEqual(t, Duration(t))

    # Verify the the Duration string output
    def test_str(self):
        for each in self.map:
            self.assertEqual(each[2], Duration(each[0]).__str__())

    # Verify the result of to_milliseconds method
    def test_to_millisecond(self):
        for each in self.map:
            self.assertEqual(each[3], Duration(each[1]).to_milliseconds())
