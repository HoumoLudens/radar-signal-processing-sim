from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


def plot_rd_map(rd_power_db: np.ndarray, ranges_m: np.ndarray, velocities_mps: np.ndarray):
    fig = px.imshow(
        rd_power_db,
        x=ranges_m,
        y=velocities_mps,
        origin="lower",
        aspect="auto",
        labels={"x": "Range (m)", "y": "Velocity (m/s)", "color": "Power (dB)"},
        title="Range-Doppler Map",
    )
    return fig


def plot_music_spectrum(angle_grid_deg: np.ndarray, spectrum: np.ndarray) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(angle_grid_deg, spectrum, lw=1.2)
    ax.set_xlabel("Angle (deg)")
    ax.set_ylabel("Normalized Spectrum")
    ax.set_title("MUSIC Spectrum")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
