"""Parse CHANnel<n>:WAVeform1:DATA:HEADer? (manual Table 17-2)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class WaveformHeader:
    x_start_s: float
    x_stop_s: float
    record_length: int
    vals_per_sample: int

    def time_axis(self) -> np.ndarray:
        return np.linspace(self.x_start_s, self.x_stop_s, self.record_length, dtype=np.float64)

    def expected_array_length(self) -> int:
        return self.record_length * self.vals_per_sample


def parse_header(raw: str) -> WaveformHeader:
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) < 4:
        raise ValueError(f"Expected 4 header fields, got {len(parts)}: {raw!r}")
    return WaveformHeader(
        x_start_s=float(parts[0]),
        x_stop_s=float(parts[1]),
        record_length=int(float(parts[2])),
        vals_per_sample=int(float(parts[3])),
    )
