from __future__ import annotations

import numpy as np


def ca_cfar_1d(power: np.ndarray, guard_cells: int = 2, train_cells: int = 12, pfa: float = 1e-4) -> tuple[np.ndarray, np.ndarray]:
    n = power.size
    threshold = np.full(n, np.nan, dtype=float)
    detections = np.zeros(n, dtype=bool)
    num_train = 2 * train_cells
    alpha = num_train * (pfa ** (-1.0 / num_train) - 1.0)

    for i in range(train_cells + guard_cells, n - train_cells - guard_cells):
        left = power[i - guard_cells - train_cells : i - guard_cells]
        right = power[i + guard_cells + 1 : i + guard_cells + train_cells + 1]
        noise = np.mean(np.concatenate([left, right]))
        threshold[i] = alpha * noise
        detections[i] = power[i] > threshold[i]

    return threshold, detections


def os_cfar_1d(power: np.ndarray, guard_cells: int = 2, train_cells: int = 12, rank: int | None = None, scale: float = 1.5) -> tuple[np.ndarray, np.ndarray]:
    n = power.size
    threshold = np.full(n, np.nan, dtype=float)
    detections = np.zeros(n, dtype=bool)
    rank = rank or train_cells

    for i in range(train_cells + guard_cells, n - train_cells - guard_cells):
        left = power[i - guard_cells - train_cells : i - guard_cells]
        right = power[i + guard_cells + 1 : i + guard_cells + train_cells + 1]
        train = np.sort(np.concatenate([left, right]))
        noise = train[min(rank, train.size - 1)]
        threshold[i] = noise * scale
        detections[i] = power[i] > threshold[i]

    return threshold, detections


def cfar_2d(rd_power: np.ndarray, guard_r: int = 1, guard_d: int = 1, train_r: int = 4, train_d: int = 4, pfa: float = 1e-4) -> np.ndarray:
    rows, cols = rd_power.shape
    detections = np.zeros_like(rd_power, dtype=bool)

    train_total = (2 * (train_r + guard_r) + 1) * (2 * (train_d + guard_d) + 1) - (2 * guard_r + 1) * (2 * guard_d + 1)
    alpha = train_total * (pfa ** (-1.0 / train_total) - 1.0)
    rd_lin = 10.0 ** (rd_power / 10.0)

    for r in range(train_r + guard_r, rows - train_r - guard_r):
        for d in range(train_d + guard_d, cols - train_d - guard_d):
            r0, r1 = r - train_r - guard_r, r + train_r + guard_r + 1
            d0, d1 = d - train_d - guard_d, d + train_d + guard_d + 1
            window = rd_lin[r0:r1, d0:d1].copy()
            g0, g1 = train_r, train_r + 2 * guard_r + 1
            h0, h1 = train_d, train_d + 2 * guard_d + 1
            window[g0:g1, h0:h1] = 0.0
            noise = window.sum() / train_total
            thr = alpha * noise
            detections[r, d] = rd_lin[r, d] > thr

    return detections
