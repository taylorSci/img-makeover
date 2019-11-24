# standard libraries
from pathlib import Path

# 3rd-party libraries
import numpy as np

########################################################################################################################

HOLDER_PATH = Path("C:\\Users\\Taylor\\Desktop\\")

########################################################################################################################


def scale(mat, oMin=0, oMax=1, optIMin=None, optIMax=None, truncateRange=True):
    """Scale matrix."""
    #TODO Raise warning if mat is unary but either optIMin and/or optIMax are not given
    if optIMin is None:
        iMin = np.min(mat)
    else:
        iMin = optIMin
    if optIMax is None:
        iMax = np.max(mat)
    else:
        iMax = optIMax
    if oMin == iMin and oMax == iMax:  # No scaling necessary
        return mat

    range_ = iMax - iMin
    scaled = (mat - iMin) / range_ * oMax + oMin
    if truncateRange:
        if isinstance(mat, np.ndarray):
            scaled[scaled < oMin] = oMin
            scaled[scaled > oMax] = oMax
        else:
            scaled = max(scaled, oMin)
            scaled = min(scaled, oMax)

    return scaled


def rgb_to_hsl(input_):
    """Convert an RGB dataset to HSL.
    Interprets 1-2D input as set of values; interprets 3D input as image.
    Last dimension should be RGB.
    RGB ranges [0,255].
    Hue ranges (0,6]; 0 is grey.
    Saturation and lightness range [0,1]."""
    assert 3 <= input_.shape[-1] <= 4, "RGB dimension should be last."
    if input_.shape[-1] == 4:
       input_ = input_[:, :, :3]  # Strip the alpha, if present

    input_ = scale(input_, optIMin=0, optIMax=255)
    max_ = np.max(input_, axis=-1)
    maxInds = np.argmax(input_, axis=-1)
    min_ = np.min(input_, axis=-1)
    delta = max_ - min_
    lightness = (max_ + min_) / 2
    chroma = delta / (1 - np.abs(2 * lightness - 1))
    chroma[np.isnan(chroma)] = 0  # Black/white
    hue = np.zeros_like(chroma)

    if input_.ndim == 3:  # Process as image
        for y in range(input_.shape[0]):
            for x in range(input_.shape[1]):
                if delta[y, x] == 0:
                    hue[y, x] = 0
                elif maxInds[y, x] == 0:
                    hue[y, x] = ((input_[y, x, 1] - input_[y, x, 2]) / delta[y, x]) % 6
                elif maxInds[y, x] == 1:
                    hue[y, x] = (input_[y, x, 2] - input_[y, x, 0]) / delta[y, x] + 2
                elif maxInds[y, x] == 2:
                    hue[y, x] = (input_[y, x, 0] - input_[y, x, 1]) / delta[y, x] + 4

    elif input_.ndim == 2:  # Process as set
        for i in range(len(input_)):
            if delta[i] == 0:
                hue[i] = 0
            elif maxInds[i] == 0:
                hue[i] = ((input_[i, 1] - input_[i, 2]) / delta[i]) % 6
            elif maxInds[i] == 1:
                hue[i] = (input_[i, 2] - input_[i, 0]) / delta[i] + 2
            elif maxInds[i] == 2:
                hue[i] = (input_[i, 0] - input_[i, 1]) / delta[i] + 4

    elif input_.ndim == 1:  # Process as individual
        if delta == 0:
            hue = 0
        elif maxInds == 0:
            hue = ((input_[1] - input_[2]) / delta) % 6
        elif maxInds == 1:
            hue = (input_[2] - input_[0]) / delta + 2
        elif maxInds == 2:
            hue = (input_[0] - input_[1]) / delta + 4

    hsl = np.stack((hue, chroma, lightness), axis=-1)
    return hsl


def hsl_to_rgb(input_):
    """Convert an HSL dataset to RGB.
    Interprets 1-2D input as set of values; interprets 3D input as image.
    Last dimension should be HSL.
    RGB ranges [0,255].
    Hue ranges (0,6]; 0 is grey.
    Saturation and lightness range [0,1]."""

    assert input_.shape[-1] == 3, "Last dimension should be the HSL."

    if input_.ndim == 3:  # Interpret as image
        hue = input_[:, :, 0]
        sat = input_[:, :, 1]
        lig = input_[:, :, 2]
        delta = sat * (1 - np.abs(2*lig - 1))
        out = delta * (1 - np.abs(hue % 2 - 1))
        floor = lig - delta/2
        rgb = np.zeros_like(input_)
        for y in range(input_.shape[0]):
            for x in range(input_.shape[1]):
                if hue[y,x] < 1:
                    rgb[y,x,:] = [delta[y,x], out[y,x], 0]
                elif hue[y,x] < 2:
                    rgb[y,x,:] = [out[y,x], delta[y,x], 0]
                elif hue[y,x] < 3:
                    rgb[y,x,:] = [0, delta[y,x], out[y,x]]
                elif hue[y,x] < 4:
                    rgb[y,x,:] = [0, out[y,x], delta[y,x]]
                elif hue[y,x] < 5:
                    rgb[y,x,:] = [out[y,x], 0, delta[y,x]]
                elif hue[y,x] < 6:
                    rgb[y,x,:] = [delta[y,x], 0, out[y,x]]
                rgb[y,x,:] += floor[y,x]
        rgb = (rgb*255).astype('uint8')

    if input_.ndim == 2:  # Interpret as set
        hue = input_[:, 0]
        sat = input_[:, 1]
        lig = input_[:, 2]
        delta = sat * (1 - np.abs(2*lig - 1))
        out = delta * (1 - np.abs(hue % 2 - 1))
        floor = lig - delta/2
        rgb = np.zeros_like(input_)
        for i in range(len(input_)):
            if 0 <= hue[i] < 1:
                rgb[i,:] = [delta[i], out[i], 0]
            elif hue[i] < 2:
                rgb[i,:] = [out[i], delta[i], 0]
            elif hue[i] < 3:
                rgb[i,:] = [0, delta[i], out[i]]
            elif hue[i] < 4:
                rgb[i,:] = [0, out[i], delta[i]]
            elif hue[i] < 5:
                rgb[i,:] = [out[i], 0, delta[i]]
            elif hue[i] < 6:
                rgb[i,:] = [delta[i], 0, out[i]]
            rgb[i,:] += floor[i]
        rgb = (rgb*255).astype('uint8')

    if input_.ndim == 1:  # Interpret as individual
        hue = input_[0]
        sat = input_[1]
        lig = input_[2]
        delta = sat * (1 - np.abs(2 * lig - 1))
        out = delta * (1 - np.abs(hue % 2 - 1))
        floor = lig - delta / 2
        if hue < 1:
            rgb = [delta, out, 0]
        elif hue < 2:
            rgb = [out, delta, 0]
        elif hue < 3:
            rgb = [0, delta, out]
        elif hue < 4:
            rgb = [0, out, delta]
        elif hue < 5:
            rgb = [out, 0, delta]
        elif hue < 6:
            rgb = [delta, 0, out]
        rgb += floor
        rgb = (rgb * 255).astype('uint8')

    return rgb