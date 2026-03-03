from __future__ import annotations

import numpy as np

from src.core.radar_params import RadarParams
from src.utils.window_functions import get_window


def doppler_fft(range_bins_complex: np.ndarray, params: RadarParams, window: str = "hann", n_fft: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    n_fft = n_fft or params.num_chirps
    win = get_window(window, params.num_chirps)
    weighted = range_bins_complex * win[:, None]
    rd = np.fft.fftshift(np.fft.fft(weighted, n=n_fft, axis=0), axes=0)
    doppler_freq = np.fft.fftshift(np.fft.fftfreq(n_fft, d=params.chirp_period_s))
    velocity_axis = doppler_freq * params.wavelength_m / 2.0
    return velocity_axis, rd


def range_doppler_map(range_spectrum: np.ndarray, params: RadarParams, window: str = "hann") -> tuple[np.ndarray, np.ndarray]:
    velocity_axis, rd_complex = doppler_fft(range_spectrum, params, window=window)
    rd_power = 20.0 * np.log10(np.abs(rd_complex) + 1e-12)
    return velocity_axis, rd_power
