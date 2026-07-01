"""Instrument setup configuration models."""

from mxo4_sigcapture.config.acquire import AcquireConfig, AcquireType, InterpolationMode, RateMode
from mxo4_sigcapture.config.app import AppConfig, ConnectionConfig, UserPrefs
from mxo4_sigcapture.config.horizontal import HorizontalConfig
from mxo4_sigcapture.config.trigger import TriggerConfig, TriggerMode, TriggerSlope, TriggerSource
from mxo4_sigcapture.config.vertical import ChannelConfig, Coupling, Impedance

__all__ = [
    "AcquireConfig",
    "AcquireType",
    "AppConfig",
    "ChannelConfig",
    "ConnectionConfig",
    "Coupling",
    "HorizontalConfig",
    "Impedance",
    "InterpolationMode",
    "RateMode",
    "TriggerConfig",
    "TriggerMode",
    "TriggerSlope",
    "TriggerSource",
    "UserPrefs",
]
