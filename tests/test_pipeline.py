import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.channel_model import Target, simulate_if_signal
from src.core.radar_params import RadarParams
from src.processing.cfar import ca_cfar_1d
from src.processing.doppler_fft import range_doppler_map
from src.processing.range_fft import range_fft


def test_range_fft_peak_near_truth():
    params = RadarParams()
    target_range = 10.0
    if_data = simulate_if_signal(params, [Target(range_m=target_range, velocity_mps=0.0, amplitude=1.0)])
    ranges, spec = range_fft(if_data, params)
    peak_range = ranges[np.argmax(np.abs(spec[0]))]
    assert abs(peak_range - target_range) < 2.0


def test_rd_map_shape_and_cfar_detects_peak():
    params = RadarParams(num_chirps=64)
    if_data = simulate_if_signal(params, [Target(range_m=25.0, velocity_mps=5.0, amplitude=1.0)])
    _, spec = range_fft(if_data, params)
    _, rd = range_doppler_map(spec, params)
    assert rd.shape[1] == params.num_adc_samples // 2

    range_bin = np.argmax(np.max(rd, axis=0))
    profile = 10 ** (rd[:, range_bin] / 10.0)
    _, det = ca_cfar_1d(profile)
    assert det.any()
