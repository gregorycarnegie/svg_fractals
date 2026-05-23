import re

import numpy as np


def lsystem(axioms: str, rules: dict, iterations: int) -> str:
    for _ in range(iterations):
        axioms = ''.join(rules.get(axiom, axiom) for axiom in axioms)
    return axioms


def append_instructions(
    n: int | float,
    c: float,
    w: str,
    x: int | float | np.float64,
    y: int | float | np.float64,
    z: np.ndarray,
    dtype: type,
) -> tuple[np.float64, np.float64, np.ndarray]:
    if dtype in {int, np.int_}:
        a = np.sin([n + .5 * np.pi, n]).astype(int)
    else:
        a = np.sin([n + .5 * np.pi, n])
    x += w * np.dot(a, c)
    y -= w * np.dot(np.fliplr([a])[0], c)
    z = np.append(z, [[x, y]], axis=0)
    return x, y, z


def reduce_instructions(
    x: int | float | np.float64,
    y: int | float | np.float64,
    z: np.ndarray,
    mult: tuple,
    constant: float,
    sequence: str,
    theta: float,
    c,
    dtype: type,
) -> np.ndarray:
    for i in range(2, -1, -1):
        sequence = re.sub('F' * mult[i][0], mult[i][1], sequence)

    w = constant * np.array([mult[0][0], mult[1][0], mult[2][0]])

    n = 0
    for char in sequence:
        if char == '+':
            n += theta
        for i in range(len(w)):
            if char == mult[i][1]:
                x, y, z = append_instructions(n, c, w[i], x, y, z, dtype)
        if char == '_':
            n -= theta
    return z


def generate_sequence(
    a0: str,
    a: str,
    b: str,
    axiom_a: str,
    axiom_b: str,
    x: float,
    y: float,
    order: int,
) -> tuple[str, np.ndarray]:
    sequence = lsystem(a0, {a: axiom_a, b: axiom_b}, order)
    sequence = re.sub('[+_][_+]', '', sequence)
    return re.sub(f'[{a}{b}]', '', sequence), np.array([[x, y]])


def hilbert(step_length: int | float, order: int) -> np.ndarray:
    constant = step_length * (pow(0.5, order))
    x, y = step_length * (pow(0.5, order + 1) - 0.5), step_length * (0.5 - pow(0.5, order + 1))
    sequence, z = generate_sequence('A', 'A', 'B', '+BF_AFA_FB+', '_AF+BFB+FA_', x, y, order)
    return reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, 0.5 * np.pi, (1, 0), int)


def gosper(step_length: int | float, order: int, x, y) -> np.ndarray:
    constant = step_length * (pow(0.5, 3))
    z = np.array([[x, y]])
    sequence = lsystem('A', {'A': 'A_B__B+A++AA+B_', 'B': '+A_BB__B_A++A+B'}, order)
    sequence = re.sub('[AB]', 'F', sequence)
    return reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, np.pi / 3, (0, 1), float)


def peano(step_length: int | float, order: int) -> np.ndarray:
    constant = 0.95 * step_length / (pow(3, order) - 1)
    x = y = 0.5 * step_length * 0.95
    sequence, z = generate_sequence('L', 'L', 'R', 'LFRFL_F_RFLFR+F+LFRFL', 'RFLFR+F+LFRFL_F_RFLFR', x, y, order)
    return reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (5, 'C')), constant, sequence, 0.5 * np.pi, (0, 1), int)


def moore(step_length: int | float, order: int) -> np.ndarray:
    constant = step_length / (pow(2, order + 1))
    x, y = -constant * 0.5, (step_length - constant) * 0.5
    sequence, z = generate_sequence('LFL+F+LFL', 'L', 'R', '_RF+LFL+FR_', '+LF_RFR_FL+', x, y, order)
    return reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, 0.5 * np.pi, (0, 1), int)
