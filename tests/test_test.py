"""A test to prevent exit code 5 in pytest runs on push."""
# pylint: disable=unspecified-encoding
from pathlib import Path


def is_docker():
    """Determines if the file is being run in a Docker container"""
    cgroup = Path('/proc/self/cgroup')
    return (
        Path('/.dockerenv').is_file()
        or cgroup.is_file()
        and cgroup.read_text().find('docker') > -1
    )


def test_test():
    """A single test to ensure pytest is working"""
    in_docker = is_docker()
    if in_docker:
        assert bool(1) is False
    else:
        assert bool(1) is True
