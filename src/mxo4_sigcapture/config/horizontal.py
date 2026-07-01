"""Horizontal / timebase configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mxo4_sigcapture.scpi.session import Mxo4Session


@dataclass
class HorizontalConfig:
    time_scale_s_per_div: float = 1e-3
    horizontal_position_s: float = 0.0
    reference_percent: float = 50.0


def apply_horizontal(session: Mxo4Session, cfg: HorizontalConfig) -> None:
    session.write(f"TIMebase:SCALe {cfg.time_scale_s_per_div}")
    session.write(f"TIMebase:REFerence {cfg.reference_percent}")
    session.write(f"TIMebase:HORizontal:POSition {cfg.horizontal_position_s}")


def query_time_scale(session: Mxo4Session) -> float:
    return float(session.query("TIMebase:SCALe?"))
