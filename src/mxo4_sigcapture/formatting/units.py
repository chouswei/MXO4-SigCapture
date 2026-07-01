"""SI display helpers for GUI readbacks and HDF5 metadata."""

from __future__ import annotations

import math

_PREFIXES = (
    (1e12, "T"),
    (1e9, "G"),
    (1e6, "M"),
    (1e3, "k"),
    (1, ""),
    (1e-3, "m"),
    (1e-6, "µ"),
    (1e-9, "n"),
    (1e-12, "p"),
)


def _scale_value(value: float, unit: str = "") -> tuple[float, str]:
    if value == 0 or not math.isfinite(value):
        return value, ""
    sign = -1 if value < 0 else 1
    v = abs(value)
    for scale, prefix in _PREFIXES:
        if v >= scale or scale == _PREFIXES[-1][0]:
            scaled = sign * v / scale
            if scaled >= 100:
                return scaled, prefix
            if scaled >= 10:
                return round(scaled, 2), prefix
            return round(scaled, 3), prefix
    return value, ""


def format_seconds(seconds: float, *, per_div: bool = False) -> str:
    scaled, prefix = _scale_value(seconds)
    suffix = "/div" if per_div else ""
    if prefix == "" and abs(scaled) < 1:
        scaled, prefix = _scale_value(seconds)
    return f"{scaled:g} {prefix}s{suffix}".replace("  ", " ").strip()


def format_sample_rate(hz: float) -> str:
    scaled, prefix = _scale_value(hz)
    return f"{scaled:g} {prefix}Sa/s".replace("  ", " ").strip()


def format_sample_rate_filename(hz: float) -> str:
    """File-safe Sa/s label, e.g. 1G25, 500M."""
    if hz <= 0 or not math.isfinite(hz):
        return "0"
    for scale, prefix in _PREFIXES:
        if hz >= scale:
            val = hz / scale
            if val == int(val):
                return f"{int(val)}{prefix}"
            whole = int(val)
            frac = int(round((val - whole) * 100))
            if frac == 0:
                return f"{whole}{prefix}"
            return f"{whole}{prefix}{frac:02d}".rstrip("0")
    return f"{hz:.0f}"


def format_points(n: int | float) -> str:
    scaled, prefix = _scale_value(float(n))
    if prefix:
        return f"{scaled:g} {prefix}pts"
    return f"{int(n)} pts"


def format_volts(volts: float, *, per_div: bool = False) -> str:
    value, unit = format_volts_parts(volts, per_div=per_div)
    return f"{value} {unit}".strip()


def format_volts_parts(volts: float, *, per_div: bool = False) -> tuple[str, str]:
    scaled, prefix = _scale_value(volts)
    suffix = "/div" if per_div else ""
    return f"{scaled:g}", f"{prefix}V{suffix}"


def format_percent(value: float) -> str:
    return f"{value:g} %"
