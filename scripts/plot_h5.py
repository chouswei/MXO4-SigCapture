#!/usr/bin/env python3
"""Plot HDF5 capture round-trip."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mxo4_sigcapture.storage.hdf5 import Hdf5Loader

CHANNEL_COLOURS = {1: "#FFCC00", 2: "#00CC66", 3: "#3399FF", 4: "#FF66CC"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plot MXO4 HDF5 capture")
    parser.add_argument("h5_path", type=Path, help="Path to .h5 file")
    parser.add_argument("--save", type=Path, help="Save figure to path")
    parser.add_argument("--no-show", action="store_true", help="Do not open interactive window")
    args = parser.parse_args(argv)

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required: pip install matplotlib", file=sys.stderr)
        return 1

    cap = Hdf5Loader().load(args.h5_path)
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    for spine in ax.spines.values():
        spine.set_color("#444444")

    for ch_num, data in sorted(cap.channels.items()):
        t = data["time"]
        y = data["y"]
        colour = CHANNEL_COLOURS.get(ch_num, "white")
        ax.plot(t, y, color=colour, label=f"C{ch_num}", linewidth=0.8)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(cap.attrs.get("instrument_idn", "MXO4 capture"), color="white")
    ax.legend(facecolor="#2a2a2a", edgecolor="#444444", labelcolor="white")
    ax.grid(True, color="#333333", linestyle="--", linewidth=0.5)
    fig.tight_layout()

    if args.save:
        fig.savefig(args.save, facecolor=fig.get_facecolor())
        print(f"Saved {args.save}")
    if not args.no_show:
        plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
