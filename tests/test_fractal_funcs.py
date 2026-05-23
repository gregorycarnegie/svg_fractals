import svgwrite
import pytest

from fractals.fractal_funcs import _add_pattern, _make_drawing


# --- _make_drawing ---

def test_make_drawing_returns_drawing():
    dwg = _make_drawing('test.svg', 'white')
    assert isinstance(dwg, svgwrite.Drawing)


def test_make_drawing_has_background_element():
    dwg = _make_drawing('test.svg', 'black')
    assert len(dwg.elements) > 0


# --- _add_pattern ---

@pytest.mark.parametrize('pattern', ['hilbert', 'gosper', 'peano', 'moore'])
def test_add_pattern_known_patterns_do_not_raise(pattern):
    dwg = _make_drawing('test.svg', 'white')
    _add_pattern(dwg, pattern, 'black', 1)


def test_add_pattern_unknown_raises_value_error():
    dwg = _make_drawing('test.svg', 'white')
    with pytest.raises(ValueError, match='Unknown pattern'):
        _add_pattern(dwg, 'ellipses', 'black', 1)


def test_add_pattern_adds_element_to_drawing():
    dwg = _make_drawing('test.svg', 'white')
    before = len(dwg.elements)
    _add_pattern(dwg, 'hilbert', 'black', 1)
    assert len(dwg.elements) > before
