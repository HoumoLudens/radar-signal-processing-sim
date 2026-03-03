from __future__ import annotations

import numpy as np

from src.core.radar_params import C, RadarParams
from src.utils.window_functions import get_window


def range_fft(if_data: np.ndarray, params: RadarParams, window: str = "hann", n_fft: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    n_fft = n_fft or params.num_adc_samples
    win = get_window(window, params.num_adc_samples)
    weighted = if_data * win[None, :]
    spectrum = np.fft.fft(weighted, n=n_fft, axis=1)
    freqs = np.fft.fftfreq(n_fft, d=1.0 / params.sample_rate_hz)
    ranges = (freqs * C) / (2.0 * params.slope_hz_per_s)
    return ranges[: n_fft // 2], spectrum[:, : n_fft // 2]
