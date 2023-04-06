"""A test to prevent exit code 5 in pytest runs on push."""


def test_test():
    """A single test to ensure pytest is working"""
    assert bool(1) is True
