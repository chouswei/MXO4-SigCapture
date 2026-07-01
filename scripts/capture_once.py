#!/usr/bin/env python3
"""Headless single-shot capture smoke test."""

from __future__ import annotations

import argparse
import json
import sys

from mxo4_sigcapture.capture.service import CaptureService
from mxo4_sigcapture.config.app import AppConfig, ConnectionConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MXO4 single-shot capture")
    parser.add_argument(
        "--resource",
        default="TCPIP0::localhost::hislip0::INSTR",
        help="VISA resource string",
    )
    parser.add_argument("--channel", type=int, default=1, help="Channel to enable")
    parser.add_argument("--json", action="store_true", help="Print summary as JSON")
    args = parser.parse_args(argv)

    cfg = AppConfig(connection=ConnectionConfig(resource=args.resource))
    for ch in cfg.channels:
        ch.enabled = ch.channel == args.channel

    try:
        from mxo4_sigcapture.scpi.session import Mxo4Session
    except ImportError as exc:
        print(f"Import error: {exc}", file=sys.stderr)
        return 1

    try:
        with Mxo4Session.from_visa(args.resource) as session:
            svc = CaptureService(session)
            errs = svc.connect(cfg)
            if any(not e.startswith("+0,") for e in errs):
                print("Connect errors:", errs, file=sys.stderr)
            result = svc.capture_once(cfg)
    except Exception as exc:
        print(f"Capture failed: {exc}", file=sys.stderr)
        return 2

    summary = {
        "idn": result.idn,
        "channels": [
            {
                "ch": w.channel,
                "points": len(w.y),
                "x_start_s": w.header.x_start_s,
                "x_stop_s": w.header.x_stop_s,
            }
            for w in result.waveforms
        ],
        "setup_errors": result.setup_errors,
        "capture_errors": result.capture_errors,
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"IDN: {result.idn}")
        for w in result.waveforms:
            print(f"CH{w.channel}: {len(w.y)} samples [{w.header.x_start_s}, {w.header.x_stop_s}] s")
        if result.setup_errors or result.capture_errors:
            print("Errors:", result.setup_errors + result.capture_errors, file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
