import pytest
from syllable_shaker import WordGenerator

def test_new_generator_fail():
    with pytest.raises(TypeError):
        WordGenerator()

def test_new_generator_empty():
    with pytest.raises(Exception):
        WordGenerator([])

@pytest.mark.parametrize("input_list,expected_size",[
    (['a'], 1),
    (['b', 'c'], 1),
    (['d', 'ef'], 2),
    (['ghi', 'jkl'], 1),
    (['m', 'no', 'pqr'], 3),
    (['s', 'tuv', 'wxy', 'z'], 2)
    ])
def test_new_generator_list(input_list, expected_size):
    gen = WordGenerator.FromList(input_list)
    assert gen is not None
    assert len(gen._syllables) == expected_size

@pytest.mark.parametrize("input_code,expected_word",[
    ('1.0', 's'),
    ('3.1', 'wxy'),
    ('3.0-1.1', 'tuvz'),
    ('1.0-1.1-1.0', 'szs')
    ])
def test_word_from_code(input_code, expected_word):
    gen = WordGenerator.FromList(['s', 'tuv', 'wxy', 'z'])
    assert gen is not None
    assert gen.MakeWordFromCode(input_code, 'no') == expected_word