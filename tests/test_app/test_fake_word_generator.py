"""Test the Fake Word Generator Class"""
from app.core.fake_word_generator import FakeWordGenerator


def test_fake_word_generator():
    """A test to show that the Fake Word Generator is able to generate plausible fake words."""
    pool = ['Hello', 'Goodbye', 'Greetings']
    fwg = FakeWordGenerator(pool, seed=2)
    output = fwg.generate(limit=3, threshold=0)
    assert output == ['Helings', 'Greetlo', 'Goodtings']
