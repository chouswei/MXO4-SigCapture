"""Trigger configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mxo4_sigcapture.scpi.session import Mxo4Session


class TriggerMode(str, Enum):
    AUTO = "AUTO"
    NORMAL = "NORMal"
    FREE_RUN = "FREerun"


class TriggerSlope(str, Enum):
    POSITIVE = "POSitive"
    NEGATIVE = "NEGative"
    EITHER = "EITHer"


class TriggerSource(str, Enum):
    CH1 = "CHANnel1"
    CH2 = "CHANnel2"
    CH3 = "CHANnel3"
    CH4 = "CHANnel4"
    EXT = "EXTernal"


@dataclass
class TriggerConfig:
    mode: TriggerMode = TriggerMode.NORMAL
    source: TriggerSource = TriggerSource.CH1
    level_v: float = 0.0
    slope: TriggerSlope = TriggerSlope.POSITIVE

    @property
    def source_channel(self) -> int:
        if self.source.value.startswith("CHANnel"):
            return int(self.source.value.replace("CHANnel", ""))
        return 1


def apply_trigger(session: Mxo4Session, cfg: TriggerConfig) -> None:
    session.write(f"TRIGger:MODE {cfg.mode.value}")
    session.write("TRIGger:EVENt1:TYPE EDGE")
    session.write(f"TRIGger:EVENt1:SOURce {cfg.source.value}")
    ch = cfg.source_channel
    session.write(f"TRIGger:EVENt1:LEVel{ch} {cfg.level_v}")
    session.write(f"TRIGger:EVENt1:EDGE:SLOPe {cfg.slope.value}")


def find_trigger_level(session: Mxo4Session) -> None:
    session.write("TRIGger:FINDlevel")
    session.opc()
