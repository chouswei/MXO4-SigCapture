"""SCPI catalog types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandInfo:
    name: str
    page: int
    usage: str = "rw"
    summary: str = ""
    parameters: tuple[str, ...] = ()
    return_values: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    rst_default: str = ""
    scpi_confirmed: bool = False
    async_cmd: bool = False

    @property
    def is_query(self) -> bool:
        return self.usage == "query" or self.name.endswith("?")

    @property
    def is_set_only(self) -> bool:
        return self.usage == "set"

    @property
    def is_event(self) -> bool:
        return self.usage in ("event", "async")

    def format_query(self) -> str:
        base = self.name.rstrip("?")
        return base if self.name.endswith("?") else f"{base}?"

    def format_set(self, *args: str | int | float) -> str:
        if self.is_query and not args:
            return self.format_query()
        base = self.name.rstrip("?")
        if not args:
            return base
        return f"{base} {','.join(str(a) for a in args)}"
