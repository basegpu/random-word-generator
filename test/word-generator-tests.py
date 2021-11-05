import pytest
from app import *

def test_new_generator_fail():
    with pytest.raises(TypeError):
        WordGenerator()

def test_new_generator_list():
    gen = WordGenerator([])