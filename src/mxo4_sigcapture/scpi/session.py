"""High-level MXO4 remote-control session."""

from __future__ import annotations

from mxo4_sigcapture.scpi.catalog import ScpiCatalog
from mxo4_sigcapture.scpi.connection import ScpiTransport, SocketTransport, VisaTransport
from mxo4_sigcapture.scpi.errors import check_error_queue


class Mxo4Session:
    """SCPI session with catalog-backed helpers and named recipes."""

    def __init__(self, transport: ScpiTransport, catalog: ScpiCatalog | None = None) -> None:
        self._io = transport
        self.cat = catalog or ScpiCatalog.default()
        self._idn: str | None = None
        self._options: str | None = None

    @classmethod
    def from_visa(cls, resource: str, *, timeout_ms: int = 60_000, **kwargs) -> "Mxo4Session":
        return cls(VisaTransport(resource, timeout_ms=timeout_ms, **kwargs))

    @classmethod
    def from_socket(cls, host: str, port: int = 5025, *, timeout_ms: int = 60_000, **kwargs) -> "Mxo4Session":
        timeout_s = timeout_ms / 1000.0
        return cls(SocketTransport(host, port, timeout_s=timeout_s, **kwargs))

    @classmethod
    def from_rs_instrument(cls, resource: str, *, timeout_ms: int = 60_000) -> "Mxo4Session":
        from mxo4_sigcapture.scpi.rs_transport import RsInstrumentTransport
        return cls(RsInstrumentTransport(resource, timeout_ms=timeout_ms))

    @property
    def timeout_ms(self) -> int:
        return self._io.timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, value: int) -> None:
        self._io.timeout_ms = value

    def close(self) -> None:
        self._io.close()

    def __enter__(self) -> "Mxo4Session":
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def write(self, command: str) -> None:
        self._io.write(command)

    def query(self, command: str) -> str:
        return self._io.query(command)

    def query_binary(self, command: str) -> bytes:
        return self._io.query_binary(command)

    def opc(self) -> str:
        return self.query("*OPC?")

    def identify(self) -> str:
        if self._idn is None:
            self._idn = self.query("*IDN?")
        return self._idn

    def options(self) -> str:
        if self._options is None:
            self._options = self.query("*OPT?")
        return self._options

    def connect_preamble(self, *, display_update: bool = True, clear_status: bool = True) -> list[str]:
        if clear_status:
            self.write("*CLS")
        self.write(f"SYSTem:DISPlay:UPDate {'ON' if display_update else 'OFF'}")
        self.identify()
        self.options()
        return check_error_queue(self)

    def reset(self) -> None:
        self.write("*RST")
        self.opc()

    def run_recipe(self, name: str, **params) -> list[str]:
        steps = self.cat.recipe_steps(name, **params)
        responses: list[str] = []
        for step in steps:
            if step.endswith("?"):
                responses.append(self.query(step))
            else:
                self.write(step)
        return responses

    def write_opc(self, command: str) -> None:
        self.write(command)
        self.opc()

    def query_after_write(self, write_cmd: str, query_cmd: str) -> str:
        self.write(write_cmd)
        return self.query(query_cmd)

    def enable_channel(self, channel: int) -> None:
        self.write(f"CHANnel{channel}:STATe 1")

    def disable_channel(self, channel: int) -> None:
        self.write(f"CHANnel{channel}:STATe 0")

    def set_vertical(self, channel: int, volts_per_div: float, offset_v: float = 0.0) -> None:
        self.write(f"CHANnel{channel}:SCALe {volts_per_div}")
        if offset_v:
            self.write(f"CHANnel{channel}:OFFSet {offset_v}")

    def set_horizontal(self, sec_per_div: float, position_s: float = 0.0) -> None:
        self.write(f"TIMebase:SCALe {sec_per_div}")
        if position_s:
            self.write(f"TIMebase:HORizontal:POSition {position_s}")

    def run_continuous(self) -> None:
        self.write("RUN")

    def run_single(self) -> None:
        self.write("RUNsingle")
        self.opc()

    def stop(self) -> None:
        self.write("STOP")

    def fetch_channel_ascii(self, channel: int) -> tuple[str, str]:
        """Return (header, data) for channel waveform in ASCII."""
        self.write("FORMat:DATA ASCii,0")
        header = self.query(f"CHANnel{channel}:WAVeform1:DATA:HEADer?")
        data = self.query(f"CHANnel{channel}:WAVeform1:DATA:VALues?")
        return header, data

    def help(self, command: str) -> str:
        return self.cat.help_text(command)
