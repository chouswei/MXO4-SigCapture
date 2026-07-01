"""Four-channel vertical configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mxo4_sigcapture.scpi.session import Mxo4Session


class Coupling(str, Enum):
    DC = "DC"
    AC = "AC"
    GND = "GND"


class Impedance(str, Enum):
    FIFTY = "FIFTy"
    ONE_MEG = "ONEMeg"


@dataclass
class ChannelConfig:
    channel: int
    enabled: bool = True
    scale_v_per_div: float = 1.0
    offset_v: float = 0.0
    position_div: float = 0.0
    coupling: Coupling = Coupling.DC
    impedance: Impedance = Impedance.FIFTY
    invert: bool = False

    def scpi_channel(self) -> str:
        return f"CHANnel{self.channel}"


def apply_channel(session: Mxo4Session, cfg: ChannelConfig) -> None:
    ch = cfg.scpi_channel()
    session.write(f"{ch}:STATe {1 if cfg.enabled else 0}")
    if not cfg.enabled:
        return
    session.write(f"{ch}:SCALe {cfg.scale_v_per_div}")
    session.write(f"{ch}:OFFSet {cfg.offset_v}")
    session.write(f"{ch}:POSition {cfg.position_div}")
    session.write(f"{ch}:COUPling {cfg.coupling.value}")
    session.write(f"{ch}:IMPedance {cfg.impedance.value}")
    session.write(f"{ch}:INVert {1 if cfg.invert else 0}")


def query_attenuation(session: Mxo4Session, channel: int) -> float:
    raw = session.query(f"CHANnel{channel}:EATT[:VALue]?")
    try:
        return float(raw)
    except ValueError:
        return 1.0
