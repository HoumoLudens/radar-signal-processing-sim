from __future__ import annotations

import numpy as np


def _steering_vector(num_ant: int, angle_deg: float, d_over_lambda: float = 0.5) -> np.ndarray:
    n = np.arange(num_ant)
    phase = 2j * np.pi * d_over_lambda * n * np.sin(np.deg2rad(angle_deg))
    return np.exp(phase)


def dbf_spectrum(snapshot: np.ndarray, angle_grid_deg: np.ndarray, d_over_lambda: float = 0.5) -> np.ndarray:
    num_ant = snapshot.size
    power = np.zeros_like(angle_grid_deg, dtype=float)
    for idx, angle in enumerate(angle_grid_deg):
        a = _steering_vector(num_ant, angle, d_over_lambda)
        power[idx] = np.abs(np.vdot(a, snapshot)) ** 2
    return power


def music_spectrum(X: np.ndarray, angle_grid_deg: np.ndarray, num_sources: int = 1, d_over_lambda: float = 0.5) -> np.ndarray:
    num_ant, num_snapshots = X.shape
    R = (X @ X.conj().T) / max(num_snapshots, 1)
    eigvals, eigvecs = np.linalg.eigh(R)
    order = np.argsort(eigvals)
    noise_space = eigvecs[:, order[: max(num_ant - num_sources, 1)]]

    spectrum = np.zeros_like(angle_grid_deg, dtype=float)
    for idx, angle in enumerate(angle_grid_deg):
        a = _steering_vector(num_ant, angle, d_over_lambda)
        denom = np.linalg.norm(noise_space.conj().T @ a) ** 2 + 1e-12
        spectrum[idx] = 1.0 / denom

    return spectrum / np.max(spectrum)
