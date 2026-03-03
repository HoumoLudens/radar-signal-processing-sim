from __future__ import annotations

from dataclasses import replace

from src.core.radar_params import RadarParams


def update_params(base: RadarParams, bandwidth_ghz: float, chirp_us: float, chirps: int) -> RadarParams:
    return replace(
        base,
        bandwidth_hz=bandwidth_ghz * 1e9,
        chirp_duration_s=chirp_us * 1e-6,
        num_chirps=chirps,
    )
