"""Acquisition configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mxo4_sigcapture.scpi.session import Mxo4Session


class AcquireType(str, Enum):
    SAMPLE = "SAMPle"
    PEAK = "PDETect"
    HIRES = "HRESolution"
    AVERAGE = "AVERage"
    ENVELOPE = "ENVelope"

    @classmethod
    def from_alias(cls, value: str) -> AcquireType:
        upper = value.upper()
        if upper in ("NORM", "NORMAL", "SAMP", "SAMPLE"):
            return cls.SAMPLE
        for member in cls:
            if member.value.upper() == upper or member.name == upper:
                return member
        return cls(value)


class InterpolationMode(str, Enum):
    SINC = "SINX"
    LINEAR = "LINear"
    SMHD = "SMHD"


class RateMode(str, Enum):
    MANUAL = "MANual"
    AUTO = "AUTO"


@dataclass
class AcquireConfig:
    acquire_type: AcquireType = AcquireType.SAMPLE
    interpolation: InterpolationMode = InterpolationMode.SINC
    points_mode: RateMode = RateMode.MANUAL
    record_length: int = 100_000
    sample_rate_mode: RateMode = RateMode.MANUAL
    sample_rate_hz: float = 1e9


def apply_acquire(session: Mxo4Session, cfg: AcquireConfig) -> None:
    session.write(f"ACQuire:TYPE {cfg.acquire_type.value}")
    session.write(f"ACQuire:INTerpolation {cfg.interpolation.value}")
    session.write(f"ACQuire:POINts:MODE {cfg.points_mode.value}")
    if cfg.points_mode == RateMode.MANUAL:
        session.write(f"ACQuire:POINts {cfg.record_length}")
    session.write(f"ACQuire:SRATe:MODE {cfg.sample_rate_mode.value}")
    if cfg.sample_rate_mode == RateMode.MANUAL:
        session.write(f"ACQuire:SRATe {cfg.sample_rate_hz}")


@dataclass
class AcquireReadback:
    sample_rate_hz: float
    record_length: int
    adc_sample_rate_hz: float
    time_scale_s_per_div: float


def query_acquire_readback(session: Mxo4Session) -> AcquireReadback:
    return AcquireReadback(
        sample_rate_hz=float(session.query("ACQuire:SRATe?")),
        record_length=int(float(session.query("ACQuire:POINts?"))),
        adc_sample_rate_hz=float(session.query("ACQuire:POINts:ARATe?")),
        time_scale_s_per_div=float(session.query("TIMebase:SCALe?")),
    )
