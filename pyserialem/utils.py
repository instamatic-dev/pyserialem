from pathlib import Path

import numpy as np
import tifffile
import yaml
from numpy.fft import fft2
from numpy.fft import ifft2


def bin_ndarray(ndarray, new_shape=None, binning=1, operation='mean'):
    """Bins an ndarray in all axes based on the target shape, by summing or
    averaging. If no target shape is given, calculate the target shape by the
    given binning.

    Number of output dimensions must match number of input dimensions and
        new axes must divide old ones.

    Example
    -------
    >>> m = np.arange(0,100,1).reshape((10,10))
    >>> n = bin_ndarray(m, new_shape=(5,5), operation='sum')
    >>> print(n)

    [[ 22  30  38  46  54]
     [102 110 118 126 134]
     [182 190 198 206 214]
     [262 270 278 286 294]
     [342 350 358 366 374]]
    """
    if not new_shape:
        shape_x, shape_y = ndarray.shape
        new_shape = int(shape_x / binning), int(shape_y / binning)

    if new_shape == ndarray.shape:
        return ndarray

    operation = operation.lower()
    if operation not in ['sum', 'mean']:
        raise ValueError('Operation not supported.')
    if ndarray.ndim != len(new_shape):
        raise ValueError(f'Shape mismatch: {ndarray.shape} -> {new_shape}')
    compression_pairs = [(d, c // d) for d, c in zip(new_shape,
                                                     ndarray.shape)]
    flattened = [l for p in compression_pairs for l in p]
    ndarray = ndarray.reshape(flattened)
    for i in range(len(new_shape)):
        op = getattr(ndarray, operation)
        ndarray = op(-1 * (i + 1))
    return ndarray


def translation(im0,
                im1,
                limit_shift: bool = False,
                return_fft: bool = False,
                ):
    """Return translation vector to register images.

    Parameters
    ----------
    im0, im1 : np.array
        The two images to compare
    limit_shift : bool
        Limit the maximum shift to the minimum array length or width.
    return_fft : bool
        Whether to additionally return the cross correlation array between the 2 images

    Returns
    -------
    shift: list
        Return the 2 coordinates defining the determined image shift
    """
    f0 = fft2(im0)
    f1 = fft2(im1)
    ir = abs(ifft2((f0 * f1.conjugate()) / (abs(f0) * abs(f1))))
    shape = ir.shape

    if limit_shift:
        min_shape = min(shape)
        shift = int(min_shape / 2)
        ir2 = np.roll(ir, (shift, shift), (0, 1))
        ir2 = ir2[:min_shape, :min_shape]
        t0, t1 = np.unravel_index(np.argmax(ir2), ir2.shape)
        t0 -= shift
        t1 -= shift
    else:
        t0, t1 = np.unravel_index(np.argmax(ir), shape)
        if t0 > shape[0] // 2:
            t0 -= shape[0]
        if t1 > shape[1] // 2:
            t1 -= shape[1]

    if return_fft:
        return [t0, t1], ir
    else:
        return [t0, t1]
