import random
import secrets

import svgwrite

from . import utils
from .data import COLOURS, PATTERNS

LENGTH = 1e3
SVG_SIZE_W = SVG_SIZE_H = LENGTH
LENGTH_ARRAY = [LENGTH / n for n in range(1, 101)]

_STROKE_DIVISOR = {'hilbert': 20, 'gosper': 20, 'peano': 40, 'moore': 20}

# Iteration range used by random mode. Gosper (3,3) means always 3.
_RANDOM_ITERATION_RANGE = {'hilbert': (1, 5), 'gosper': (3, 3), 'peano': (1, 3), 'moore': (0, 3)}

# Iteration range exposed to the UI slider per pattern.
ITERATION_RANGES = {'hilbert': (1, 6), 'gosper': (1, 4), 'peano': (1, 3), 'moore': (1, 4)}

_COLOUR_KEYS = list(COLOURS.keys())
_COLOUR_WEIGHTS = list(COLOURS.values())
_PATTERN_KEYS = list(PATTERNS.keys())
_PATTERN_WEIGHTS = list(PATTERNS.values())


def _make_drawing(file_name: str, background_fill: str) -> svgwrite.Drawing:
    result = svgwrite.Drawing(file_name, (SVG_SIZE_W, SVG_SIZE_H), profile='full', debug=True)
    result.viewbox(-SVG_SIZE_W / 2, -SVG_SIZE_H / 2, SVG_SIZE_W, SVG_SIZE_H)
    result.add(result.rect(insert=(-LENGTH_ARRAY[1], -LENGTH_ARRAY[1]), size=('100%', '100%'), fill=background_fill))
    return result


def _add_pattern(result: svgwrite.Drawing, pattern: str, colour: str, iterations: int) -> None:
    if pattern not in _STROKE_DIVISOR:
        raise ValueError(f'Unknown pattern {pattern!r}. Choose from: {", ".join(_STROKE_DIVISOR)}')
    stroke_width = int(LENGTH / (_STROKE_DIVISOR[pattern] * (iterations + 1)))
    if pattern == 'hilbert':
        pts = utils.hilbert(LENGTH, iterations)
    elif pattern == 'gosper':
        pts = utils.gosper(5 * LENGTH / 4, iterations, 5 * LENGTH / 4, 0)
    elif pattern == 'peano':
        pts = utils.peano(LENGTH, iterations)
    elif pattern == 'moore':
        pts = utils.moore(LENGTH, iterations)
    result.add(result.polyline(points=pts, fill='none', stroke_width=stroke_width, stroke=colour))


def generate(pattern: str, background: str, colour: str, iterations: int) -> str:
    """Return SVG XML string for the given settings."""
    dwg = _make_drawing('preview', background)
    _add_pattern(dwg, pattern, colour, iterations)
    return dwg.tostring()


def random_settings() -> dict:
    """Return a random set of fractal settings."""
    random.seed(secrets.randbits(32))
    background = random.choices(_COLOUR_KEYS, weights=_COLOUR_WEIGHTS)[0]
    pattern = random.choices(_PATTERN_KEYS, weights=_PATTERN_WEIGHTS)[0]
    other_colours = [c for c in _COLOUR_KEYS if c != background]
    other_weights = [COLOURS[c] for c in other_colours]
    colour = random.choices(other_colours, weights=other_weights)[0]
    lo, hi = _RANDOM_ITERATION_RANGE[pattern]
    iterations = random.randint(lo, hi)
    return {'pattern': pattern, 'background': background, 'colour': colour, 'iterations': iterations}


def fractal(file_name: str) -> svgwrite.Drawing:
    iterations = int(input('How many iterations? '))
    background_fill = input('Background colour: ')
    pattern_choice = input('Pattern (Hilbert / Gosper / Moore / Peano): ').lower()
    pattern_colour = input('Pattern colour: ')

    while pattern_colour == background_fill:
        confirm = input('Pattern and background are the same colour. Continue? (y/n): ')
        if confirm.lower() in {'y', 'yes'}:
            break
        background_fill = input('Background colour: ')
        pattern_colour = input('Pattern colour: ')

    result = _make_drawing(file_name, background_fill)
    _add_pattern(result, pattern_choice, pattern_colour, iterations)
    return result


def random_fractal(file_name: str) -> svgwrite.Drawing:
    s = random_settings()
    result = _make_drawing(file_name, s['background'])
    _add_pattern(result, s['pattern'], s['colour'], s['iterations'])
    return result
