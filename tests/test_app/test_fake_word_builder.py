"""Test the Fake Word Builder Class"""
from app.core.fake_word_builder import FakeWordBuilder


def test_fake_word_builder():
    """A test to show that the Fake Word Builder is able to generate plausible fake words."""
    pool = ['Hello', 'Goodbye', 'Greetings']
    fwb = FakeWordBuilder(pool, seed=2)
    output = fwb.generate(limit=3, threshold=0)
    assert output == ['Helings', 'Greetlo', 'Goodtings']
