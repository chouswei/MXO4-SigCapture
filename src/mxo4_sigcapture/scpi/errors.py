"""SCPI error queue discipline."""

from __future__ import annotations

from typing import Protocol


class ScpiQueryable(Protocol):
    def query(self, command: str) -> str: ...


def check_error_queue(session: ScpiQueryable) -> list[str]:
    """Drain SYSTem:ERRor:NEXT? until +0,\"No error\"."""
    messages: list[str] = []
    while True:
        raw = session.query("SYSTem:ERRor:NEXT?").strip()
        messages.append(raw)
        if raw.startswith("+0,") or raw.startswith("0,"):
            break
        if '"No error"' in raw and (raw.startswith("+0") or raw.startswith("0")):
            break
    return messages


def raise_if_errors(session: ScpiQueryable) -> None:
    """Raise RuntimeError if the error queue contains non-zero entries."""
    messages = check_error_queue(session)
    errors = [m for m in messages if not (m.startswith("+0,") or m.startswith("0,"))]
    if errors:
        raise RuntimeError("SCPI error queue: " + "; ".join(errors))
