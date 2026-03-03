from __future__ import annotations

import numpy as np


def add_awgn(signal: np.ndarray, snr_db: float, rng: np.random.Generator | None = None) -> np.ndarray:
    rng = rng or np.random.default_rng()
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = signal_power / (10.0 ** (snr_db / 10.0))
    noise = (
        rng.normal(0.0, np.sqrt(noise_power / 2.0), size=signal.shape)
        + 1j * rng.normal(0.0, np.sqrt(noise_power / 2.0), size=signal.shape)
    )
    return signal + noise


def add_ground_clutter(signal: np.ndarray, clutter_level_db: float = -20.0, rng: np.random.Generator | None = None) -> np.ndarray:
    rng = rng or np.random.default_rng()
    clutter_scale = 10.0 ** (clutter_level_db / 20.0)
    clutter = clutter_scale * (
        rng.normal(size=signal.shape) + 1j * rng.normal(size=signal.shape)
    )
    return signal + clutter
