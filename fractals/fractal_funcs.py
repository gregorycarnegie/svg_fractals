import random

import numpy as np
import pandas as pd
import quantumrandom as qr
import svgwrite

from . import utils

"""DATA"""
COLOURS = pd.read_excel('DATA.xlsx', sheet_name='Sheet1')
COLOUR_LIST = utils.ratio(COLOURS['Colour Names'], COLOURS['Numbers'])
COLOUR_NAMES = COLOURS['SVG name']
PATTERNS = pd.read_excel('DATA.xlsx', sheet_name='Sheet2')
PATTERN_LIST = utils.ratio(PATTERNS['Pattern'], PATTERNS['Numbers'])

LENGTH = 1e3
SVG_SIZE_W = SVG_SIZE_H = LENGTH
LENGTH_ARRAY = np.array([1.0] + [LENGTH / n for n in range(1, 101)])

def fractal(file_name: str):
    iterations = int(input('How many iterations do you need?'))
    # Canvas
    result = svgwrite.Drawing(file_name, (SVG_SIZE_W, SVG_SIZE_H), profile='full', debug=True)
    result.viewbox(-SVG_SIZE_W / 2, -SVG_SIZE_H / 2, SVG_SIZE_W, SVG_SIZE_H)
    # Background
    background_fill = input('What colour background do you want?')
    result.add(result.rect(insert=(-LENGTH_ARRAY[2], -LENGTH_ARRAY[2]), size=('100%', '100%'), fill=background_fill))
    # Pattern Choices
    pattern_choice = input(
        """
        Please choose from the below list:
        - Hilbert
        - Gosper
        - Moore
        - Peano
        """
    ).lower()
    pattern_choice_col = input('What colour do you want the pattern to be?')
    loop = True
    while loop:
        if pattern_choice_col == background_fill:
            escape = input('The pattern and the background are the same colour\n'
                           'Are you sure this is what you want?')
            if escape.lower() in {'y', 'yes'}:
                loop = False
            else:
                background_fill = input('What colour background do you want?')
                pattern_choice_col = input('What colour do you want the pattern to be?')
                if pattern_choice_col == background_fill:
                    escape = input('The pattern and the background are the same colour\n'
                                   'Are you sure this is what you want?')
                    if escape.lower() in {'y', 'yes'}:
                        loop = False
        else:
            loop = False

    if pattern_choice == 'hilbert':
        pl = result.polyline(points=utils.hilbert(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))), stroke=pattern_choice_col)
        result.add(pl)
    elif pattern_choice == 'gosper':
        pl = result.polyline(points=utils.gosper(5 * LENGTH / 4, iterations, 5 * LENGTH / 4, 0), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))), stroke=pattern_choice_col)
        result.add(pl)
    elif pattern_choice == 'peano':
        pl = result.polyline(points=utils.peano(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (40 * (iterations + 1))), stroke=pattern_choice_col)
        result.add(pl)
    if pattern_choice == 'moore':
        pl = result.polyline(points=utils.moore(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))), stroke=pattern_choice_col)
        result.add(pl)

    return result

def random_fractal(file_name: str):
    random.seed(qr.randint(1, 5_000_000_000))
    # Canvas
    result = svgwrite.Drawing(file_name, (SVG_SIZE_W, SVG_SIZE_H), profile='full', debug=True)
    result.viewbox(-SVG_SIZE_W / 2, -SVG_SIZE_H / 2, SVG_SIZE_W, SVG_SIZE_H)
    # Background
    background_fill = random.choice(COLOUR_LIST[:-20])
    result.add(result.rect(insert=(-LENGTH_ARRAY[2], -LENGTH_ARRAY[2]), size=('100%', '100%'), fill=background_fill))
    # Pattern Choices
    pattern_choice = random.choice(PATTERN_LIST)
    pattern_choice_col = [x for x in COLOUR_LIST[:-20] if x != background_fill]
    if pattern_choice == 'Hilbert':
        iterations = random.randint(1, 5)
        pl = result.polyline(points=utils.hilbert(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))),
                             stroke=random.choice(pattern_choice_col))
        result.add(pl)
    elif pattern_choice == 'Gosper':
        iterations = 3
        pl = result.polyline(points=utils.gosper(5 * LENGTH / 4, iterations, 5 * LENGTH / 4, 0), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))),
                             stroke=random.choice(pattern_choice_col))
        result.add(pl)
    elif pattern_choice == 'Peano':
        iterations = random.randint(1, 3)
        pl = result.polyline(points=utils.peano(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (40 * (iterations + 1))),
                             stroke=random.choice(pattern_choice_col))
        result.add(pl)
    if pattern_choice == 'Moore':
        iterations = random.randint(0, 3)
        pl = result.polyline(points=utils.moore(LENGTH, iterations), fill='none',
                             stroke_width=int(LENGTH / (20 * (iterations + 1))),
                             stroke=random.choice(pattern_choice_col))
        result.add(pl)
    return result
