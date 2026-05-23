import numpy as np
import pytest

from fractals.utils import (
    append_instructions,
    generate_sequence,
    hilbert,
    gosper,
    lsystem,
    moore,
    peano,
)


# --- lsystem ---

def test_lsystem_zero_iterations_returns_axiom():
    assert lsystem('A', {'A': 'AB', 'B': 'A'}, 0) == 'A'


def test_lsystem_one_iteration():
    assert lsystem('A', {'A': 'AB', 'B': 'A'}, 1) == 'AB'


def test_lsystem_two_iterations():
    assert lsystem('A', {'A': 'AB', 'B': 'A'}, 2) == 'ABA'


def test_lsystem_unknown_symbols_pass_through():
    assert lsystem('AF', {'A': 'B'}, 1) == 'BF'


# --- fractal generators ---

@pytest.mark.parametrize('order', [1, 2, 3])
def test_hilbert_returns_2d_array(order):
    pts = hilbert(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_hilbert_more_points_with_higher_order():
    assert len(hilbert(100, 2)) > len(hilbert(100, 1))


@pytest.mark.parametrize('order', [1, 2, 3])
def test_gosper_returns_2d_array(order):
    pts = gosper(100, order, 100, 0)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_gosper_more_points_with_higher_order():
    assert len(gosper(100, 2, 100, 0)) > len(gosper(100, 1, 100, 0))


@pytest.mark.parametrize('order', [1, 2])
def test_peano_returns_2d_array(order):
    pts = peano(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_peano_more_points_with_higher_order():
    assert len(peano(100, 2)) > len(peano(100, 1))


@pytest.mark.parametrize('order', [1, 2, 3])
def test_moore_returns_2d_array(order):
    pts = moore(100, order)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2
    assert pts.shape[1] == 2


def test_moore_more_points_with_higher_order():
    assert len(moore(100, 2)) > len(moore(100, 1))
