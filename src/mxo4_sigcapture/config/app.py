"""Top-level application configuration."""

from __future__ import annotations

from dataclasses import dataclass, field

from mxo4_sigcapture.config.acquire import AcquireConfig
from mxo4_sigcapture.config.horizontal import HorizontalConfig
from mxo4_sigcapture.config.trigger import TriggerConfig
from mxo4_sigcapture.config.vertical import ChannelConfig


@dataclass
class ConnectionConfig:
    resource: str = "TCPIP0::localhost::hislip0::INSTR"
    visa_timeout_ms: int = 60_000
    opc_timeout_ms: int = 10_000


@dataclass
class UserPrefs:
    display_update: bool = True
    auto_apply_before_capture: bool = False
    last_save_dir: str = "data/captures"


@dataclass
class AppConfig:
    connection: ConnectionConfig = field(default_factory=ConnectionConfig)
    channels: list[ChannelConfig] = field(default_factory=lambda: [
        ChannelConfig(1, scale_v_per_div=0.5),
        ChannelConfig(2, enabled=False),
        ChannelConfig(3, enabled=False),
        ChannelConfig(4, enabled=False),
    ])
    horizontal: HorizontalConfig = field(default_factory=HorizontalConfig)
    acquire: AcquireConfig = field(default_factory=AcquireConfig)
    trigger: TriggerConfig = field(default_factory=TriggerConfig)
    prefs: UserPrefs = field(default_factory=UserPrefs)

    def enabled_channels(self) -> list[ChannelConfig]:
        return [c for c in self.channels if c.enabled]

    def copy(self) -> AppConfig:
        import copy
        return copy.deepcopy(self)
