from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

C = 299_792_458.0


@dataclass(slots=True)
class RadarParams:
    carrier_freq_hz: float = 77.0e9
    bandwidth_hz: float = 4.0e9
    chirp_duration_s: float = 40.0e-6
    idle_time_s: float = 10.0e-6
    sample_rate_hz: float = 20.0e6
    num_adc_samples: int = 512
    num_chirps: int = 128
    num_rx_antennas: int = 8
    noise_figure_db: float = 5.0
    temperature_k: float = 290.0

    @property
    def slope_hz_per_s(self) -> float:
        return self.bandwidth_hz / self.chirp_duration_s

    @property
    def wavelength_m(self) -> float:
        return C / self.carrier_freq_hz

    @property
    def chirp_period_s(self) -> float:
        return self.chirp_duration_s + self.idle_time_s

    @property
    def range_resolution_m(self) -> float:
        return C / (2.0 * self.bandwidth_hz)

    @property
    def velocity_resolution_mps(self) -> float:
        return self.wavelength_m / (2.0 * self.num_chirps * self.chirp_period_s)

    @property
    def max_unambiguous_range_m(self) -> float:
        return self.sample_rate_hz * C * self.chirp_duration_s / (2.0 * self.bandwidth_hz)

    @property
    def max_unambiguous_velocity_mps(self) -> float:
        return self.wavelength_m / (4.0 * self.chirp_period_s)

    @classmethod
    def from_yaml(cls, file_path: str | Path) -> "RadarParams":
        content: dict[str, Any] = yaml.safe_load(Path(file_path).read_text(encoding="utf-8"))
        return cls(**content)
