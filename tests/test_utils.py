import numpy as np
import pytest

from fractals.utils import (
    _direction_count,
    _reduce_vector,
    _reduce_vectors,
    _turtle,
    _turtle_vectors,
    append_instructions,
    dragon,
    generate_sequence,
    hilbert,
    gosper,
    lsystem,
    moore,
    peano,
    reduce_instructions,
    sierpinski_arrowhead,
)


# --- append_instructions ---


def test_append_instructions_steps_along_x():
    # n=0 → cos(n)=1; c=(1,0) → x moves by w, y unchanged
    x, y, _ = append_instructions(
        0, (1, 0), 5.0, 0.0, 0.0, np.array([[0.0, 0.0]]), float
    )
    assert np.isclose(x, 5.0)
    assert np.isclose(y, 0.0)


def test_append_instructions_steps_along_y():
    # n=0 → c=(0,1) → y is subtracted, x unchanged
    x, y, _ = append_instructions(
        0, (0, 1), 5.0, 0.0, 0.0, np.array([[0.0, 0.0]]), float
    )
    assert np.isclose(x, 0.0)
    assert np.isclose(y, -5.0)


def test_append_instructions_appends_point_to_z():
    z0 = np.array([[0.0, 0.0]])
    x, y, z = append_instructions(0, (1, 0), 1.0, 0.0, 0.0, z0, float)
    assert z.shape == (2, 2)
    assert np.allclose(z[-1], [x, y])


def test_append_instructions_int_dtype_rounds_sin():
    # At n=π/4, sin values ≈ 0.707 → truncated to 0 by int cast, so position stays at origin
    z_float = append_instructions(
        np.pi / 4, (1, 0), 1.0, 0.0, 0.0, np.array([[0.0, 0.0]]), float
    )[2]
    z_int = append_instructions(
        np.pi / 4, (1, 0), 1.0, 0.0, 0.0, np.array([[0.0, 0.0]]), int
    )[2]
    assert not np.allclose(z_float[-1], z_int[-1])


# --- generate_sequence ---


def test_generate_sequence_returns_string_and_array():
    seq, z = generate_sequence("F", "A", "B", "A", "B", 0.0, 0.0, 0)
    assert isinstance(seq, str)
    assert isinstance(z, np.ndarray) and z.shape == (1, 2)


def test_generate_sequence_starting_point():
    _, z = generate_sequence("F", "A", "B", "A", "B", 3.5, -1.2, 0)
    assert np.allclose(z, [[3.5, -1.2]])


def test_generate_sequence_removes_letter_symbols():
    seq, _ = generate_sequence("ABA", "A", "B", "A", "B", 0.0, 0.0, 0)
    assert "A" not in seq and "B" not in seq


def test_generate_sequence_cancels_adjacent_opposite_turns():
    seq, _ = generate_sequence("+_", "A", "B", "A", "B", 0.0, 0.0, 0)
    assert seq == ""


def test_generate_sequence_hilbert_order_1():
    seq, z = generate_sequence("A", "A", "B", "+BF_AFA_FB+", "_AF+BFB+FA_", 0.0, 0.0, 1)
    assert seq == "+F_F_F+"
    assert np.allclose(z, [[0.0, 0.0]])


# --- lsystem ---


def test_lsystem_zero_iterations_returns_axiom():
    assert lsystem("A", {"A": "AB", "B": "A"}, 0) == "A"


def test_lsystem_one_iteration():
    assert lsystem("A", {"A": "AB", "B": "A"}, 1) == "AB"


def test_lsystem_two_iterations():
    assert lsystem("A", {"A": "AB", "B": "A"}, 2) == "ABA"


def test_lsystem_unknown_symbols_pass_through():
    assert lsystem("AF", {"A": "B"}, 1) == "BF"


# --- fractal generators ---


@pytest.mark.parametrize("order", [1, 2, 3])
def test_hilbert_returns_2d_array(order):
    pts = hilbert(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_hilbert_more_points_with_higher_order():
    assert len(hilbert(100, 2)) > len(hilbert(100, 1))


@pytest.mark.parametrize("order", [1, 2, 3])
def test_gosper_returns_2d_array(order):
    pts = gosper(100, order, 100, 0)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_gosper_more_points_with_higher_order():
    assert len(gosper(100, 2, 100, 0)) > len(gosper(100, 1, 100, 0))


@pytest.mark.parametrize("order", [1, 2])
def test_peano_returns_2d_array(order):
    pts = peano(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_peano_more_points_with_higher_order():
    assert len(peano(100, 2)) > len(peano(100, 1))


@pytest.mark.parametrize("order", [1, 2, 3])
def test_moore_returns_2d_array(order):
    pts = moore(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_moore_more_points_with_higher_order():
    assert len(moore(100, 2)) > len(moore(100, 1))


@pytest.mark.parametrize("order", [1, 2, 3])
def test_sierpinski_arrowhead_returns_2d_array(order):
    pts = sierpinski_arrowhead(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_sierpinski_arrowhead_more_points_with_higher_order():
    assert len(sierpinski_arrowhead(100, 2)) > len(sierpinski_arrowhead(100, 1))


@pytest.mark.parametrize("order", [1, 2, 3])
def test_dragon_returns_2d_array(order):
    pts = dragon(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_dragon_more_points_with_higher_order():
    assert len(dragon(100, 2)) > len(dragon(100, 1))


# --- _direction_count ---


def test_direction_count_right_angle():
    assert _direction_count(np.pi / 2) == 4


def test_direction_count_sixty_degrees():
    assert _direction_count(np.pi / 3) == 6


def test_direction_count_irrational_returns_none():
    assert _direction_count(1.0) is None


# --- _reduce_vector ---


def test_reduce_vector_c1_angle_zero():
    dx, dy = _reduce_vector(0.0, (1, 0), float)
    assert np.isclose(dx, 1.0) and np.isclose(dy, 0.0)


def test_reduce_vector_c1_angle_half_pi():
    dx, dy = _reduce_vector(np.pi / 2, (1, 0), float)
    assert np.isclose(dx, 0.0) and np.isclose(dy, -1.0)


def test_reduce_vector_c0_angle_zero():
    # c[0]=0 branch: dx=sin(angle), dy=-cos(angle)
    dx, dy = _reduce_vector(0.0, (0, 1), float)
    assert np.isclose(dx, 0.0) and np.isclose(dy, -1.0)


def test_reduce_vector_int_dtype_rounds():
    # cos(π/4) ≈ 0.707 → rounds to 1; -sin(π/4) ≈ -0.707 → rounds to -1
    dx, dy = _reduce_vector(np.pi / 4, (1, 0), int)
    assert dx == 1.0 and dy == -1.0


# --- _reduce_vectors ---


def test_reduce_vectors_right_angle_count():
    assert len(_reduce_vectors(np.pi / 2, (1, 0), float)) == 4


def test_reduce_vectors_irrational_returns_none():
    assert _reduce_vectors(1.0, (1, 0), float) is None


def test_reduce_vectors_c1_right_angle_directions():
    vecs = _reduce_vectors(np.pi / 2, (1, 0), float)
    assert np.allclose(vecs[0], (1.0, 0.0))
    assert np.allclose(vecs[1], (0.0, -1.0))
    assert np.allclose(vecs[2], (-1.0, 0.0))
    assert np.allclose(vecs[3], (0.0, 1.0))


def test_reduce_vectors_int_dtype_rounds():
    vecs = _reduce_vectors(np.pi / 2, (1, 0), int)
    assert all(v[0] in (-1.0, 0.0, 1.0) and v[1] in (-1.0, 0.0, 1.0) for v in vecs)


# --- _turtle_vectors ---


def test_turtle_vectors_right_angle_count():
    assert len(_turtle_vectors(np.pi / 2, 0.0)) == 4


def test_turtle_vectors_irrational_returns_none():
    assert _turtle_vectors(1.0, 0.0) is None


def test_turtle_vectors_start_angle_zero():
    vecs = _turtle_vectors(np.pi / 2, 0.0)
    assert np.allclose(vecs[0], (1.0, 0.0))
    assert np.allclose(vecs[1], (0.0, 1.0))
    assert np.allclose(vecs[2], (-1.0, 0.0))
    assert np.allclose(vecs[3], (0.0, -1.0))


def test_turtle_vectors_nonzero_start_angle():
    vecs = _turtle_vectors(np.pi / 2, np.pi / 2)
    assert np.allclose(vecs[0], (0.0, 1.0))


# --- _turtle ---


def test_turtle_single_draw_char_gives_two_points():
    pts = _turtle("F", 1.0, np.pi / 2, "F")
    assert pts.shape == (2, 2)


def test_turtle_steps_right_by_default():
    pts = _turtle("F", 5.0, np.pi / 2, "F")
    assert np.allclose(pts[0], [0.0, 0.0])
    assert np.allclose(pts[1], [5.0, 0.0])


def test_turtle_turn_changes_direction():
    # F then + then F: first step right, turn left (y+), second step up
    pts = _turtle("F+F", 1.0, np.pi / 2, "F")
    assert pts.shape == (3, 2)
    assert np.allclose(pts[2], [1.0, 1.0])


def test_turtle_non_draw_chars_ignored():
    pts = _turtle("X", 1.0, np.pi / 2, "F")
    assert pts.shape == (1, 2)
    assert np.allclose(pts[0], [0.0, 0.0])


# --- reduce_instructions ---


def test_reduce_instructions_single_f_steps_right():
    z = np.array([[0.0, 0.0]])
    pts = reduce_instructions(
        0.0, 0.0, z, ((1, "A"), (2, "B"), (3, "C")), 1.0, "F", np.pi / 2, (1, 0), int
    )
    assert pts.shape == (2, 2)
    assert np.allclose(pts[1], [1.0, 0.0])


def test_reduce_instructions_ff_uses_b_width():
    # 'FF' → substituted to 'B' (length 2) → one step of width 2
    z = np.array([[0.0, 0.0]])
    pts = reduce_instructions(
        0.0, 0.0, z, ((1, "A"), (2, "B"), (3, "C")), 1.0, "FF", np.pi / 2, (1, 0), int
    )
    assert pts.shape == (2, 2)
    assert np.allclose(pts[1], [2.0, 0.0])


def test_reduce_instructions_turn():
    z = np.array([[0.0, 0.0]])
    pts = reduce_instructions(
        0.0, 0.0, z, ((1, "A"), (2, "B"), (3, "C")), 1.0, "F+F", np.pi / 2, (1, 0), int
    )
    assert pts.shape == (3, 2)
    assert np.allclose(pts[1], [1.0, 0.0])
    assert np.allclose(pts[2], [1.0, -1.0])
