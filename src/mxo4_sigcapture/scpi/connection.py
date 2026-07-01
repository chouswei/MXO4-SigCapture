"""VISA/socket transport for MXO4."""

from __future__ import annotations

from typing import Protocol


class ScpiTransport(Protocol):
    @property
    def timeout_ms(self) -> int: ...

    @timeout_ms.setter
    def timeout_ms(self, value: int) -> None: ...

    def write(self, command: str) -> None: ...
    def read(self) -> str: ...
    def query(self, command: str) -> str: ...
    def query_binary(self, command: str) -> bytes: ...
    def close(self) -> None: ...


def _parse_definite_block(payload: bytes) -> bytes:
    """Parse IEEE 488.2 definite-length block (#N...)."""
    if not payload or payload[0:1] != b"#":
        return payload
    ndigits = int(chr(payload[1]))
    header_len = 2 + ndigits
    data_len = int(payload[2:header_len].decode())
    return payload[header_len : header_len + data_len]


class VisaTransport:
    """PyVISA wrapper (resource string e.g. TCPIP::host::hislip0::INSTR)."""

    def __init__(self, resource: str, *, timeout_ms: int = 10_000) -> None:
        try:
            import pyvisa
        except ImportError as exc:
            raise ImportError("pip install pyvisa pyvisa-py for instrument I/O") from exc
        self._rm = pyvisa.ResourceManager("@py")
        self._inst = self._rm.open_resource(resource)
        self._timeout_ms = timeout_ms
        self._inst.timeout = timeout_ms
        self._inst.read_termination = "\n"
        self._inst.write_termination = "\n"

    @property
    def timeout_ms(self) -> int:
        return self._timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, value: int) -> None:
        self._timeout_ms = value
        self._inst.timeout = value

    def write(self, command: str) -> None:
        self._inst.write(command)

    def read(self) -> str:
        return str(self._inst.read()).strip()

    def query(self, command: str) -> str:
        return str(self._inst.query(command)).strip()

    def query_binary(self, command: str) -> bytes:
        self.write(command)
        try:
            raw = bytes(self._inst.read_raw())
        except AttributeError:
            raw = self.read().encode()
        return _parse_definite_block(raw)

    def close(self) -> None:
        self._inst.close()
        self._rm.close()


class SocketTransport:
    """Raw TCP SCPI (default port 5025)."""

    def __init__(self, host: str, port: int = 5025, *, timeout_s: float = 10.0) -> None:
        import socket

        self._timeout_ms = int(timeout_s * 1000)
        self._sock = socket.create_connection((host, port), timeout=timeout_s)
        self._file = self._sock.makefile("rwb", buffering=0)

    @property
    def timeout_ms(self) -> int:
        return self._timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, value: int) -> None:
        self._timeout_ms = value
        self._sock.settimeout(value / 1000.0)

    def write(self, command: str) -> None:
        self._file.write((command.rstrip() + "\n").encode())

    def read(self) -> str:
        return self._file.readline().decode().strip()

    def _read_raw_block(self) -> bytes:
        first = self._file.read(1)
        if first != b"#":
            rest = self._file.readline()
            return first + rest
        ndigits = int(self._file.read(1).decode())
        length_str = self._file.read(ndigits).decode()
        data_len = int(length_str)
        return self._file.read(data_len)

    def query(self, command: str) -> str:
        self.write(command)
        return self.read()

    def query_binary(self, command: str) -> bytes:
        self.write(command)
        return _parse_definite_block(self._read_raw_block())

    def close(self) -> None:
        self._file.close()
        self._sock.close()
