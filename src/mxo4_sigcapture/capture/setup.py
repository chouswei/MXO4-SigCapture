"""Ordered instrument setup application."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mxo4_sigcapture.config.acquire import AcquireReadback, apply_acquire, query_acquire_readback
from mxo4_sigcapture.config.horizontal import apply_horizontal
from mxo4_sigcapture.config.trigger import apply_trigger
from mxo4_sigcapture.config.vertical import apply_channel
from mxo4_sigcapture.scpi.errors import check_error_queue

if TYPE_CHECKING:
    from mxo4_sigcapture.config.app import AppConfig
    from mxo4_sigcapture.scpi.session import Mxo4Session


@dataclass
class SetupResult:
    errors: list[str]
    readback: AcquireReadback | None = None


def apply_export_format(session: Mxo4Session) -> None:
    session.write("FORMat:DATA REAL,32")
    session.write("FORMat:BORDer LSBFirst")
    session.write("EXPort:WAVeform:INCXvalues OFF")


def apply_all_setup(session: Mxo4Session, config: AppConfig) -> SetupResult:
    """Apply setup in fixed expert order; drain error queue at end."""
    session.stop()
    for ch in config.channels:
        apply_channel(session, ch)
    apply_acquire(session, config.acquire)
    apply_horizontal(session, config.horizontal)
    apply_trigger(session, config.trigger)
    apply_export_format(session)
    session.opc()
    errors = check_error_queue(session)
    readback = query_acquire_readback(session)
    return SetupResult(errors=errors, readback=readback)
