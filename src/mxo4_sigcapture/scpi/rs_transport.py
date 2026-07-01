"""Optional RsInstrument transport adapter."""

from __future__ import annotations


class RsInstrumentTransport:
    """Thin ScpiTransport wrapper using Rohde-Schwarz RsInstrument binary helpers."""

    def __init__(self, resource: str, *, timeout_ms: int = 60_000) -> None:
        try:
            from RsInstrument import RsInstrument
        except ImportError as exc:
            raise ImportError("pip install RsInstrument for rs transport") from exc
        self._inst = RsInstrument(
            resource,
            reset=False,
            options="SelectVisa='rs'",
        )
        self._timeout_ms = timeout_ms
        self._inst.visa_timeout = timeout_ms

    @property
    def timeout_ms(self) -> int:
        return self._timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, value: int) -> None:
        self._timeout_ms = value
        self._inst.visa_timeout = value

    def write(self, command: str) -> None:
        self._inst.write_str(command)

    def read(self) -> str:
        return self._inst.query_str("").strip()

    def query(self, command: str) -> str:
        return self._inst.query_str(command).strip()

    def query_binary(self, command: str) -> bytes:
        data = self._inst.query_bin_or_ascii_float_list(command)
        if isinstance(data, (list, tuple)):
            import struct
            return struct.pack(f"<{len(data)}f", *data)
        return bytes(data)

    def close(self) -> None:
        self._inst.close()
