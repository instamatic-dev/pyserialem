import numpy as np
import pytest

from pyserialem import bin_ndarray


def test_binning():
    x = 32
    y = 32
    x2 = int(x / 2)
    y2 = int(y / 2)
    a = np.arange(x * y).reshape(x, y)

    b = bin_ndarray(a, new_shape=(x2, y2))
    assert b.shape == (x2, y2)

    b = bin_ndarray(a, new_shape=(x, y))
    assert b.shape == (x, y)

    b = bin_ndarray(a, binning=2)
    assert b.shape == (x2, y2)

    with pytest.raises(ValueError):
        b = bin_ndarray(a, binning=1.32)


def test_value():
    m = np.arange(0, 100, 1).reshape((10, 10))
    n = bin_ndarray(m, new_shape=(5, 5), operation='sum')
    m = np.array([
        [22, 30, 38, 46, 54],
        [102, 110, 118, 126, 134],
        [182, 190, 198, 206, 214],
        [262, 270, 278, 286, 294],
        [342, 350, 358, 366, 374],
    ])
    assert np.allclose(n, m)
