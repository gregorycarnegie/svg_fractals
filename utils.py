import re
from math import cos, sin, pi
import numpy as np


def colour_proper(proper_names, names, colour):
    return proper_names[np.where(names == colour)[0][0]]


def ratio(names, numbers):
    ratio_list = []
    for n in range(len(names)):
        ratio_list += [names[n] for _ in range(int(numbers[n]))]
    return ratio_list


def lsystem(axioms, rules, iterations):
    """We iterate through our method required numbers of time."""
    for _ in range(iterations):
        """Our newly created axioms from this iteration."""
        newAxioms = ''.join(rules[axiom] if axiom in rules else axiom for axiom in axioms)
        """
        You will need to iterate through your newAxioms next time, so...
        We transfer newAxioms, to axioms that is being iterated on, in the for loop.
        """
        axioms = newAxioms
    return axioms


def reduce_instructions(x, y, z, mult, constant, sequence, theta, A, dtype):
    sequence = re.sub('F' * mult[2][0], mult[2][1], sequence)
    sequence = re.sub('F' * mult[1][0], mult[1][1], sequence)
    sequence = re.sub('F' * mult[0][0], mult[0][1], sequence)
    w = constant * np.array([mult[0][0], mult[1][0], mult[2][0]])

    n = 0
    for char in sequence:
        if char == '+':
            n += theta
        if char == mult[0][1]:
            a = np.array([cos(n), sin(n)])
            if dtype in {int, np.int}:
                a = a.astype(int)
            x += w[0] * np.dot(a, A)
            y -= w[0] * np.dot(np.fliplr([a])[0], A)
            z = np.append(z, [[x, y]], axis=0)
        if char == mult[1][1]:
            a = np.array([cos(n), sin(n)])
            if dtype in {int, np.int}:
                a = a.astype(int)
            x += w[1] * np.dot(a, A)
            y -= w[1] * np.dot(np.fliplr([a])[0], A)
            z = np.append(z, [[x, y]], axis=0)
        if char == mult[2][1]:
            a = np.array([cos(n), sin(n)])
            if dtype in {int, np.int}:
                a = a.astype(int)
            x += w[2] * np.dot(a, A)
            y -= w[2] * np.dot(np.fliplr([a])[0], A)
            z = np.append(z, [[x, y]], axis=0)
        if char == '_':
            n -= theta
    print(sequence)
    return z


def hilbert(step_length, order):
    x = step_length * (pow(0.5, order + 1) - 0.5)
    y = step_length * (0.5 - pow(0.5, order + 1))
    constant = step_length * (pow(0.5, order))
    z = np.array([[x, y]])

    sequence = lsystem('A', {'A': '+BF_AFA_FB+', 'B': '_AF+BFB+FA_'}, order)
    sequence = re.sub('[+_][_+]', '', sequence)
    sequence = re.sub('[AB]', '', sequence)

    z = reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, 0.5 * pi, (1, 0), int)
    return z


def gosper(step_length, order, x, y):
    const = step_length * (pow(0.5, 3))
    z = np.array([[x, y]])

    sequence = lsystem('A', {'A': 'A_B__B+A++AA+B_', 'B': '+A_BB__B_A++A+B'}, order)
    sequence = re.sub('[AB]', 'F', sequence)

    z = reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), const, sequence, pi/3, (0, 1), float)
    return z


def peano(step_length, order):
    x = y = 0.5 * step_length * 0.95
    constant = 0.95 * step_length / (pow(3, order) - 1)
    z = np.array([[x, y]])

    sequence = lsystem('L', {'L': 'LFRFL_F_RFLFR+F+LFRFL', 'R': 'RFLFR+F+LFRFL_F_RFLFR'}, order)
    sequence = re.sub('[+_][_+]', '', sequence)
    sequence = re.sub('[LR]', '', sequence)

    z = reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (5, 'C')), constant, sequence, 0.5 * pi, (0, 1), int)
    return z


def moore(step_length, order):
    constant = step_length / (pow(2, order + 1))
    x = -constant / 2
    y = (step_length - constant) / 2

    z = np.array([[x, y]])

    sequence = lsystem('LFL+F+LFL', {'L': '_RF+LFL+FR_', 'R': '+LF_RFR_FL+'}, order)
    sequence = re.sub('[+_][_+]', '', sequence)
    sequence = re.sub('[LR]', '', sequence)

    z = reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, 0.5 * pi, (0, 1), int)
    return z
