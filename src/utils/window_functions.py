from __future__ import annotations

import numpy as np
from scipy.signal import windows


def get_window(name: str, length: int) -> np.ndarray:
    name_l = name.lower()
    if name_l in {"hann", "hanning"}:
        return windows.hann(length, sym=False)
    if name_l == "hamming":
        return windows.hamming(length, sym=False)
    if name_l == "blackman":
        return windows.blackman(length, sym=False)
    if name_l in {"rect", "rectangular", "none"}:
        return np.ones(length)
    raise ValueError(f"Unsupported window: {name}")
