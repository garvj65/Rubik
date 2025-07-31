"""Run all tests for the Rubik's Cube solver."""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_tests():
    """Run all tests in the tests directory."""
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)


if __name__ == "__main__":
    run_tests()