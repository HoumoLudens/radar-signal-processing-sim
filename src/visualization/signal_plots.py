from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def plot_time_waveform(signal: np.ndarray, fs_hz: float, title: str = "Time-domain IF Signal") -> plt.Figure:
    t = np.arange(signal.size) / fs_hz
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(t * 1e6, np.real(signal), lw=1.0)
    ax.set_xlabel("Time (us)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_range_profile(ranges_m: np.ndarray, spectrum: np.ndarray, chirp_idx: int = 0) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 3))
    profile_db = 20.0 * np.log10(np.abs(spectrum[chirp_idx]) + 1e-12)
    ax.plot(ranges_m, profile_db, lw=1.0)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title(f"Range Profile (chirp {chirp_idx})")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
