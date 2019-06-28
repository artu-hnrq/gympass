
# Define an decorator to wrap a test code that need to verify for an error
def expectError(expected_errors, resolve = None):
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
            finally:
                if resolve is not None:
                    resolve()

        return do
    return decorator
