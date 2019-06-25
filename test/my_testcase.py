import unittest

class MyTestCase(unittest.TestCase):

    #  General method for checking for exceptions
    def expectError(self, expected_errors, test):
        try:
            test()
        except expected_errors:
            'the expected exceptioon was raised'
        except:
            raise
        else:
            self.fail(f"Some of the followings errors were expected: {expected_errors}")
