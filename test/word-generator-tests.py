import pytest
from syllable_shaker import *

def test_new_generator_fail():
    with pytest.raises(TypeError):
        WordGenerator()

def test_new_generator_empty():
    with pytest.raises(Exception):
        WordGenerator([])

def test_new_generator_list():
    gen = WordGenerator(['a'])
    assert gen is not None
    assert len(gen._syllables[1]) == 1