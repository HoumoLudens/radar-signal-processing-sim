from __future__ import annotations

import numpy as np

from .radar_params import RadarParams


def generate_tx_chirp(params: RadarParams, t: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    if t is None:
        t = np.arange(params.num_adc_samples) / params.sample_rate_hz

    phase = 2.0 * np.pi * (params.carrier_freq_hz * t + 0.5 * params.slope_hz_per_s * t**2)
    return t, np.exp(1j * phase)


def generate_chirp_sequence(params: RadarParams) -> np.ndarray:
    _, chirp = generate_tx_chirp(params)
    return np.tile(chirp, (params.num_chirps, 1))
