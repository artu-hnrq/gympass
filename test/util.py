
# Define an decorator to wrap the test codes that need to verify for an error
def expectError(expected_errors):
    def decorator(test):
        def do(self):
            try:
                test(self)
            except expected_errors:
                'the expected exceptioon was raised'
            except:
                raise
            else:
                self.fail(f"Some of the followings errors were expected: {expected_errors}")

        return do
    return decorator
