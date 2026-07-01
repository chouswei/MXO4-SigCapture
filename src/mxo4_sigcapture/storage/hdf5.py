"""HDF5 capture storage."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from mxo4_sigcapture.capture.fetch import ChannelWaveform
from mxo4_sigcapture.capture.service import CaptureResult
from mxo4_sigcapture.config.app import AppConfig
from mxo4_sigcapture.formatting.units import format_sample_rate_filename

FILENAME_TEMPLATE = "{utc}_{trig_mode}_{srat}_{points}.h5"
FILENAME_CONVENTION_ATTR = '"{utc}_{trig_mode}_{srat}_{points}.h5"'


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_filename(config: AppConfig, result: CaptureResult) -> str:
    trig = config.trigger.mode.value.replace(" ", "")
    srat = format_sample_rate_filename(
        result.readback.sample_rate_hz if result.readback else config.acquire.sample_rate_hz
    )
    points = str(
        result.readback.record_length if result.readback else config.acquire.record_length
    )
    return FILENAME_TEMPLATE.format(utc=_utc_stamp(), trig_mode=trig, srat=srat, points=points)


def _shared_time_axis(waveforms: list[ChannelWaveform]) -> bool:
    if not waveforms:
        return False
    ref = waveforms[0].header
    if ref.vals_per_sample != 1:
        return False
    for w in waveforms[1:]:
        if w.header.vals_per_sample != 1:
            return False
        if (
            w.header.record_length != ref.record_length
            or w.header.x_start_s != ref.x_start_s
            or w.header.x_stop_s != ref.x_stop_s
        ):
            return False
    return True


@dataclass
class Hdf5Capture:
    """Loaded capture from HDF5."""

    attrs: dict[str, Any]
    time: np.ndarray | None
    channels: dict[int, dict[str, Any]]


class Hdf5Writer:
    def write(
        self,
        path: Path | str,
        config: AppConfig,
        result: CaptureResult,
    ) -> Path:
        import h5py

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        readback = result.readback
        shared = _shared_time_axis(result.waveforms)

        with h5py.File(path, "w") as f:
            f.attrs["instrument_idn"] = result.idn
            f.attrs["instrument_options"] = result.options
            f.attrs["utc_timestamp"] = _utc_stamp()
            f.attrs["filename_convention"] = FILENAME_CONVENTION_ATTR
            f.attrs["app_config_json"] = json.dumps(asdict(config), default=str)
            f.attrs["trigger_mode"] = config.trigger.mode.value
            f.attrs["acquire_type"] = config.acquire.acquire_type.value
            f.attrs["interpolate"] = config.acquire.interpolation.value
            f.attrs["time_scale_requested"] = config.horizontal.time_scale_s_per_div
            f.attrs["time_scale_actual"] = readback.time_scale_s_per_div if readback else 0.0
            f.attrs["sample_rate_requested"] = config.acquire.sample_rate_hz
            f.attrs["sample_rate_actual"] = readback.sample_rate_hz if readback else 0.0
            f.attrs["record_length_requested"] = config.acquire.record_length
            f.attrs["record_length_actual"] = readback.record_length if readback else 0
            f.attrs["adc_sample_rate"] = readback.adc_sample_rate_hz if readback else 0.0
            f.attrs["t_unit"] = "s"
            f.attrs["y_unit"] = "V"

            if shared and result.waveforms:
                f.create_dataset("time", data=result.waveforms[0].time, dtype=np.float64)

            for w in result.waveforms:
                grp = f.create_group(f"ch{w.channel}")
                grp.create_dataset("y", data=w.y, dtype=np.float32)
                hdr = grp.create_group("header")
                hdr.create_dataset("x_start_s", data=w.header.x_start_s)
                hdr.create_dataset("x_stop_s", data=w.header.x_stop_s)
                hdr.create_dataset("record_length", data=w.header.record_length)
                hdr.create_dataset("vals_per_sample", data=w.header.vals_per_sample)
                if not shared:
                    grp.create_dataset("time", data=w.time, dtype=np.float64)
                if w.attenuation != 1.0:
                    grp.attrs["attenuation"] = w.attenuation
        return path


class Hdf5Loader:
    def load(self, path: Path | str) -> Hdf5Capture:
        import h5py

        path = Path(path)
        with h5py.File(path, "r") as f:
            attrs = {k: f.attrs[k] for k in f.attrs}
            time_ds = f["time"][:] if "time" in f else None
            channels: dict[int, dict[str, Any]] = {}
            for key in f.keys():
                if not key.startswith("ch"):
                    continue
                ch_num = int(key.replace("ch", ""))
                grp = f[key]
                ch_time = grp["time"][:] if "time" in grp else time_ds
                hdr_grp = grp["header"]
                channels[ch_num] = {
                    "y": grp["y"][:],
                    "time": ch_time,
                    "header": {
                        "x_start_s": float(hdr_grp["x_start_s"][()]),
                        "x_stop_s": float(hdr_grp["x_stop_s"][()]),
                        "record_length": int(hdr_grp["record_length"][()]),
                        "vals_per_sample": int(hdr_grp["vals_per_sample"][()]),
                    },
                    "attrs": dict(grp.attrs),
                }
        return Hdf5Capture(attrs=attrs, time=time_ds, channels=channels)
