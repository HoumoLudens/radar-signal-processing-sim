from __future__ import annotations

import os
import sys

import numpy as np
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from src.core.channel_model import Target, simulate_if_signal
from src.core.radar_params import RadarParams
from src.processing.doppler_fft import range_doppler_map
from src.processing.range_fft import range_fft

st.set_page_config(page_title="FMCW Radar Sim", layout="wide")
st.title("FMCW 毫米波雷达信号处理可视化")

params = RadarParams()
col1, col2, col3 = st.columns(3)
with col1:
    target_range = st.slider("目标距离 (m)", 5.0, 150.0, 35.0, 1.0)
with col2:
    target_vel = st.slider("目标速度 (m/s)", -30.0, 30.0, 8.0, 0.5)
with col3:
    snr_db = st.slider("SNR (dB)", -10.0, 40.0, 20.0, 1.0)

if_data = simulate_if_signal(params, [Target(range_m=target_range, velocity_mps=target_vel, amplitude=1.0)])
noise_scale = 10 ** (-snr_db / 20)
if_data = if_data + noise_scale * (np.random.randn(*if_data.shape) + 1j * np.random.randn(*if_data.shape))

ranges, range_spec = range_fft(if_data, params)
vels, rd_map = range_doppler_map(range_spec, params)

st.subheader("Range-Doppler Map")
st.image(((rd_map - rd_map.min()) / (rd_map.max() - rd_map.min() + 1e-12) * 255).astype("uint8"), clamp=True)

range_profile = 20 * np.log10(np.abs(range_spec[0]) + 1e-12)
st.subheader("Range Profile (First Chirp)")
st.line_chart({"range_db": range_profile[: min(256, range_profile.size)]})
