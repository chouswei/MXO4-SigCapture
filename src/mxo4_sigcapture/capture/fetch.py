"""Binary waveform fetch from MXO4."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import numpy as np

from mxo4_sigcapture.capture.header import WaveformHeader, parse_header
from mxo4_sigcapture.capture.setup import apply_export_format
from mxo4_sigcapture.config.vertical import query_attenuation
from mxo4_sigcapture.scpi.errors import check_error_queue

if TYPE_CHECKING:
    from mxo4_sigcapture.scpi.session import Mxo4Session


@dataclass
class ChannelWaveform:
    channel: int
    header: WaveformHeader
    y: np.ndarray
    time: np.ndarray
    attenuation: float = 1.0
    clipped: bool = False


def _decode_float32_block(data: bytes, expected_len: int) -> np.ndarray:
    if len(data) % 4 != 0:
        raise ValueError(f"Binary block length {len(data)} not multiple of 4")
    arr = np.array(struct.unpack(f"<{len(data) // 4}f", data), dtype=np.float32)
    if expected_len and len(arr) != expected_len:
        arr = arr[:expected_len]
    return arr


def fetch_channel_waveform(
    session: Mxo4Session,
    channel: int,
    *,
    chunk_size: int | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> ChannelWaveform:
    if cancel_check and cancel_check():
        raise InterruptedError("Capture cancelled")
    header_raw = session.query(f"CHANnel{channel}:WAVeform1:DATA:HEADer?")
    header = parse_header(header_raw)
    expected = header.expected_array_length()
    cmd = f"CHANnel{channel}:WAVeform1:DATA:VALues?"
    if chunk_size and expected > chunk_size:
        chunks: list[np.ndarray] = []
        offset = 0
        while offset < expected:
            if cancel_check and cancel_check():
                raise InterruptedError("Capture cancelled")
            length = min(chunk_size, expected - offset)
            block = session.query_binary(f"{cmd} {offset},{length}")
            chunks.append(_decode_float32_block(block, length))
            offset += length
        y = np.concatenate(chunks)
    else:
        block = session.query_binary(cmd)
        y = _decode_float32_block(block, expected)
    check_error_queue(session)
    time_axis = header.time_axis()
    if header.vals_per_sample == 2:
        y = y.reshape(-1, 2)[:, 0]
    ymax = float(np.max(np.abs(y))) if len(y) else 0.0
    clipped = bool(ymax > 0 and np.any(np.abs(y) >= 0.99 * ymax))
    att = query_attenuation(session, channel)
    return ChannelWaveform(
        channel=channel,
        header=header,
        y=y.astype(np.float32),
        time=time_axis,
        attenuation=att,
        clipped=clipped,
    )


def arm_single_shot(session: Mxo4Session) -> None:
    apply_export_format(session)
    session.run_single()
    check_error_queue(session)


def fetch_enabled_channels(
    session: Mxo4Session,
    channels: list[int],
    *,
    chunk_size: int | None = None,
    on_channel_start: Callable[[int, int], None] | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> list[ChannelWaveform]:
    results: list[ChannelWaveform] = []
    total = len(channels)
    for idx, ch in enumerate(channels, start=1):
        if on_channel_start:
            on_channel_start(ch, total)
        results.append(
            fetch_channel_waveform(
                session,
                ch,
                chunk_size=chunk_size,
                cancel_check=cancel_check,
            )
        )
    return results
