from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .radar_params import C, RadarParams
from .signal_generator import generate_tx_chirp


@dataclass(slots=True)
class Target:
    range_m: float
    velocity_mps: float
    amplitude: float = 1.0
    angle_deg: float = 0.0


def _rx_phase(params: RadarParams, time_fast: np.ndarray, slow_time: float, target: Target) -> np.ndarray:
    delay_s = 2.0 * (target.range_m + target.velocity_mps * slow_time) / C
    t_delayed = time_fast - delay_s
    return 2.0 * np.pi * (params.carrier_freq_hz * t_delayed + 0.5 * params.slope_hz_per_s * t_delayed**2)


def simulate_if_signal(params: RadarParams, targets: list[Target]) -> np.ndarray:
    time_fast, tx = generate_tx_chirp(params)
    if_data = np.zeros((params.num_chirps, params.num_adc_samples), dtype=np.complex128)

    for chirp_idx in range(params.num_chirps):
        slow_time = chirp_idx * params.chirp_period_s
        rx = np.zeros(params.num_adc_samples, dtype=np.complex128)
        for target in targets:
            rx += target.amplitude * np.exp(1j * _rx_phase(params, time_fast, slow_time, target))
        if_data[chirp_idx] = tx * np.conj(rx)

    return if_data
