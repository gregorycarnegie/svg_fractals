import re

import numpy as np


_FULL_TURN = 2 * np.pi


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

    widths = {char: constant * length for length, char in mult}
    points = np.empty((len(z) + sum(sequence.count(char) for char in widths), 2), dtype=float)
    points[:len(z)] = z
    point_index = len(z)

    vectors = _reduce_vectors(theta, c, dtype)
    direction = 0
    angle = 0.0

    for char in sequence:
        if char == '+':
            direction = (direction + 1) % len(vectors) if vectors is not None else direction
            angle += theta
        elif char == '_':
            direction = (direction - 1) % len(vectors) if vectors is not None else direction
            angle -= theta
        elif char in widths:
            if vectors is None:
                dx, dy = _reduce_vector(angle, c, dtype)
            else:
                dx, dy = vectors[direction]
            x += widths[char] * dx
            y += widths[char] * dy
            points[point_index] = [x, y]
            point_index += 1
    return points[:point_index]


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


def _direction_count(theta: float) -> int | None:
    count = _FULL_TURN / theta
    rounded = round(float(count))
    if rounded > 0 and np.isclose(count, rounded):
        return rounded
    return None


def _reduce_vector(angle: float, c, dtype: type) -> tuple[float, float]:
    if c[0]:
        dx, dy = np.cos(angle), -np.sin(angle)
    else:
        dx, dy = np.sin(angle), -np.cos(angle)
    if dtype in {int, np.int_}:
        return float(round(dx)), float(round(dy))
    return float(dx), float(dy)


def _reduce_vectors(theta: float, c, dtype: type) -> tuple[tuple[float, float], ...] | None:
    count = _direction_count(theta)
    if count is None:
        return None
    angles = np.arange(count) * theta
    if c[0]:
        vectors = np.column_stack((np.cos(angles), -np.sin(angles)))
    else:
        vectors = np.column_stack((np.sin(angles), -np.cos(angles)))
    if dtype in {int, np.int_}:
        vectors = np.rint(vectors)
    return tuple((float(dx), float(dy)) for dx, dy in vectors)


def _turtle_vectors(theta: float, start_angle: float) -> tuple[tuple[float, float], ...] | None:
    count = _direction_count(theta)
    if count is None:
        return None
    angles = start_angle + np.arange(count) * theta
    return tuple((float(dx), float(dy)) for dx, dy in np.column_stack((np.cos(angles), np.sin(angles))))


def _turtle(sequence: str, step: float, theta: float, draw_chars: str, start_angle: float = 0.0) -> np.ndarray:
    x, y = 0.0, 0.0
    angle = start_angle
    draw_set = set(draw_chars)
    points = np.empty((sum(ch in draw_set for ch in sequence) + 1, 2), dtype=float)
    points[0] = [x, y]
    point_index = 1
    vectors = _turtle_vectors(theta, start_angle)
    direction = 0
    for ch in sequence:
        if ch in draw_set:
            if vectors is None:
                dx, dy = np.cos(angle), np.sin(angle)
            else:
                dx, dy = vectors[direction]
            x += step * dx
            y += step * dy
            points[point_index] = [x, y]
            point_index += 1
        elif ch == '+':
            direction = (direction + 1) % len(vectors) if vectors is not None else direction
            angle += theta
        elif ch == '_':
            direction = (direction - 1) % len(vectors) if vectors is not None else direction
            angle -= theta
    return points[:point_index]


def hilbert(step_length: int | float, order: int) -> np.ndarray:
    constant = step_length * (pow(0.5, order))
    x, y = step_length * (pow(0.5, order + 1) - 0.5), step_length * (0.5 - pow(0.5, order + 1))
    sequence, z = generate_sequence('A', 'A', 'B', '+BF_AFA_FB+', '_AF+BFB+FA_', x, y, order)
    return reduce_instructions(x, y, z, ((1, 'A'), (2, 'B'), (3, 'C')), constant, sequence, 0.5 * np.pi, (1, 0), int)


def sierpinski_arrowhead(step_length: float, order: int) -> np.ndarray:
    step = step_length / pow(2, order)
    start_angle = np.pi / 3 if order % 2 else 0.0
    sequence = lsystem('A', {'A': 'B_A_B', 'B': 'A+B+A'}, order)
    return _turtle(sequence, step, np.pi / 3, 'AB', start_angle)


def dragon(step_length: float, order: int) -> np.ndarray:
    step = step_length * pow(2, -order / 2)
    sequence = lsystem('F', {'F': 'F+G', 'G': 'F_G'}, order)
    return _turtle(sequence, step, np.pi / 2, 'FG')


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
