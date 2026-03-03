from __future__ import annotations

import numpy as np


class KalmanCV2D:
    def __init__(self, dt: float, process_var: float = 1.0, meas_var: float = 4.0) -> None:
        self.dt = dt
        self.x = np.zeros((4, 1))
        self.F = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype=float)
        q = process_var
        self.Q = q * np.array(
            [[dt**4 / 4, 0, dt**3 / 2, 0], [0, dt**4 / 4, 0, dt**3 / 2], [dt**3 / 2, 0, dt**2, 0], [0, dt**3 / 2, 0, dt**2]],
            dtype=float,
        )
        self.R = meas_var * np.eye(2)
        self.P = np.eye(4) * 10.0

    def predict(self) -> np.ndarray:
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x.copy()

    def update(self, z: np.ndarray) -> np.ndarray:
        z = z.reshape(2, 1)
        y = z - self.H @ self.x
        s = self.H @ self.P @ self.H.T + self.R
        k = self.P @ self.H.T @ np.linalg.inv(s)
        self.x = self.x + k @ y
        self.P = (np.eye(4) - k @ self.H) @ self.P
        return self.x.copy()


def nearest_neighbor_association(tracks: np.ndarray, detections: np.ndarray) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    if tracks.size == 0 or detections.size == 0:
        return pairs

    used_tracks: set[int] = set()
    used_dets: set[int] = set()

    while len(used_tracks) < len(tracks) and len(used_dets) < len(detections):
        best = None
        best_dist = np.inf
        for i, trk in enumerate(tracks):
            if i in used_tracks:
                continue
            for j, det in enumerate(detections):
                if j in used_dets:
                    continue
                dist = np.linalg.norm(trk - det)
                if dist < best_dist:
                    best_dist = dist
                    best = (i, j)

        if best is None:
            break
        used_tracks.add(best[0])
        used_dets.add(best[1])
        pairs.append(best)

    return pairs
