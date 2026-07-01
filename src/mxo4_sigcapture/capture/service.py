"""High-level capture orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from mxo4_sigcapture.capture.fetch import ChannelWaveform, arm_single_shot, fetch_enabled_channels
from mxo4_sigcapture.capture.setup import SetupResult, apply_all_setup
from mxo4_sigcapture.config.acquire import AcquireReadback
from mxo4_sigcapture.config.app import AppConfig
from mxo4_sigcapture.scpi.errors import check_error_queue
from mxo4_sigcapture.scpi.session import Mxo4Session


@dataclass
class CaptureResult:
    waveforms: list[ChannelWaveform] = field(default_factory=list)
    setup_errors: list[str] = field(default_factory=list)
    capture_errors: list[str] = field(default_factory=list)
    readback: AcquireReadback | None = None
    idn: str = ""
    options: str = ""


class CaptureService:
    def __init__(self, session: Mxo4Session) -> None:
        self.session = session

    def connect(self, config: AppConfig) -> list[str]:
        self.session.timeout_ms = config.connection.visa_timeout_ms
        return self.session.connect_preamble(display_update=config.prefs.display_update)

    def apply_setup(self, config: AppConfig) -> SetupResult:
        return apply_all_setup(self.session, config)

    def capture_once(
        self,
        config: AppConfig,
        *,
        apply_first: bool = True,
        on_channel_start: Callable[[int, int], None] | None = None,
        cancel_check: Callable[[], bool] | None = None,
    ) -> CaptureResult:
        result = CaptureResult(idn=self.session.identify(), options=self.session.options())
        if apply_first:
            setup = apply_all_setup(self.session, config)
            result.setup_errors = [e for e in setup.errors if not e.startswith("+0,")]
            result.readback = setup.readback
        else:
            from mxo4_sigcapture.config.trigger import apply_trigger
            apply_trigger(self.session, config.trigger)
        arm_single_shot(self.session)
        channels = [c.channel for c in config.enabled_channels()]
        try:
            result.waveforms = fetch_enabled_channels(
                self.session,
                channels,
                on_channel_start=on_channel_start,
                cancel_check=cancel_check,
            )
        except InterruptedError:
            result.capture_errors.append("Capture cancelled by user")
        result.capture_errors.extend(
            e for e in check_error_queue(self.session) if not e.startswith("+0,")
        )
        return result
