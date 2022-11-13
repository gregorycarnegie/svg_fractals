import random

import numpy as np
import pandas as pd
import quantumrandom as qr
import svgwrite

import utils

"""DATA"""
colours = pd.read_excel('DATA.xlsx', sheet_name='Sheet1')
colour_list = np.array(utils.ratio(colours['Colour Names'], colours['Numbers']))
colour_names = colours['SVG name']
patterns = pd.read_excel('DATA.xlsx', sheet_name='Sheet2')
pattern_list = np.array(utils.ratio(patterns['Pattern'], patterns['Numbers']))

length = 1e3
svg_size_w = svg_size_h = length
length_array = np.array([1.0] + [length / n for n in range(1, 101)])


def run(file_name, choice):
    file_name = f'svgs\\{file_name}.svg'
    if choice in {'y', 'yes'}:
        random.seed(qr.randint(1, 5_000_000_000))
        # Canvas ##################################################################################################### #
        dwg = svgwrite.Drawing(file_name, (svg_size_w, svg_size_h), profile='full', debug=True)
        dwg.viewbox(-svg_size_w / 2, -svg_size_h / 2, svg_size_w, svg_size_h)
        # Background ################################################################################################# #
        background_fill = random.choice(colour_list[:-20])
        dwg.add(dwg.rect(insert=(-length_array[2], -length_array[2]), size=('100%', '100%'), fill=background_fill))
        # Pattern Choices ############################################################################################ #
        pattern_choice = random.choice(pattern_list)
        pattern_choice_col = [x for x in colour_list[:-20] if x != background_fill]
        if pattern_choice == 'Hilbert':
            iterations = random.randint(1, 5)
            pl = dwg.polyline(points=utils.hilbert(length, iterations), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=random.choice(pattern_choice_col))
            dwg.add(pl)
        elif pattern_choice == 'Gosper':
            iterations = 3
            pl = dwg.polyline(points=utils.gosper(5 * length / 4, iterations, 5 * length / 4, 0), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=random.choice(pattern_choice_col))
            dwg.add(pl)
        elif pattern_choice == 'Peano':
            iterations = random.randint(1, 3)
            pl = dwg.polyline(points=utils.peano(length, iterations), fill='none',
                              stroke_width=int(length / (40 * (iterations + 1))),
                              stroke=random.choice(pattern_choice_col))
            dwg.add(pl)
        if pattern_choice == 'Moore':
            iterations = random.randint(0, 3)
            pl = dwg.polyline(points=utils.moore(length, iterations), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=random.choice(pattern_choice_col))
            dwg.add(pl)
    else:
        iterations = int(input('How many iterations do you need?'))
        # Canvas ##################################################################################################### #
        dwg = svgwrite.Drawing(file_name, (svg_size_w, svg_size_h), profile='full', debug=True)
        dwg.viewbox(-svg_size_w / 2, -svg_size_h / 2, svg_size_w, svg_size_h)
        # Background ################################################################################################# #
        background_fill = input('What colour background do you want?')
        dwg.add(dwg.rect(insert=(-length_array[2], -length_array[2]), size=('100%', '100%'), fill=background_fill))
        # Pattern Choices ############################################################################################ #
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
            pl = dwg.polyline(points=utils.hilbert(length, iterations), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=pattern_choice_col)
            dwg.add(pl)
        elif pattern_choice == 'gosper':
            pl = dwg.polyline(points=utils.gosper(5 * length / 4, iterations, 5 * length / 4, 0), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=pattern_choice_col)
            dwg.add(pl)
        elif pattern_choice == 'peano':
            pl = dwg.polyline(points=utils.peano(length, iterations), fill='none',
                              stroke_width=int(length / (40 * (iterations + 1))),
                              stroke=pattern_choice_col)
            dwg.add(pl)
        if pattern_choice == 'moore':
            pl = dwg.polyline(points=utils.moore(length, iterations), fill='none',
                              stroke_width=int(length / (20 * (iterations + 1))),
                              stroke=pattern_choice_col)
            dwg.add(pl)

    dwg.save()


if __name__ == '__main__':
    filename = input('Please type the name of your file:')
    random_select = input('Print a random pattern (Yes/No?):').lower()
    run(filename, random_select)
