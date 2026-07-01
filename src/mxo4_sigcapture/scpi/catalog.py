"""Load and query the MXO4 SCPI catalog."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

from mxo4_sigcapture.scpi.types import CommandInfo


def _data_path(name: str) -> Path:
    return Path(__file__).parent / "data" / name


class ScpiCatalog:
    """In-process library backed by manifest + command index JSON."""

    def __init__(self, manifest: dict[str, Any], commands: list[CommandInfo]) -> None:
        self._manifest = manifest
        self._by_name = {c.name: c for c in commands}
        self._by_subsystem: dict[str, list[CommandInfo]] = {}
        for cmd in commands:
            sub = cmd.name.split(":")[0] if not cmd.name.startswith("*") else "COMMON"
            self._by_subsystem.setdefault(sub, []).append(cmd)

    @classmethod
    def load(cls, data_dir: Path | None = None) -> "ScpiCatalog":
        base = data_dir or Path(__file__).parent / "data"
        manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
        raw = json.loads((base / "commands.json").read_text(encoding="utf-8"))
        commands = [CommandInfo(**{**item, "parameters": tuple(item.get("parameters", [])), "return_values": tuple(item.get("return_values", [])), "examples": tuple(item.get("examples", []))}) for item in raw["commands"]]
        return cls(manifest, commands)

    @classmethod
    @lru_cache(maxsize=1)
    def default(cls) -> "ScpiCatalog":
        return cls.load()

    @property
    def manifest(self) -> dict[str, Any]:
        return self._manifest

    @property
    def connection(self) -> dict[str, str]:
        return self._manifest["connection"]

    @property
    def conventions(self) -> dict[str, str]:
        return self._manifest["conventions"]

    def __len__(self) -> int:
        return len(self._by_name)

    def get(self, name: str) -> CommandInfo | None:
        return self._by_name.get(name)

    def require(self, name: str) -> CommandInfo:
        cmd = self.get(name)
        if cmd is None:
            raise KeyError(f"Unknown SCPI command: {name}")
        return cmd

    def names(self) -> Iterator[str]:
        yield from sorted(self._by_name)

    def subsystem(self, prefix: str) -> list[CommandInfo]:
        return list(self._by_subsystem.get(prefix, []))

    def search(self, substring: str, *, limit: int = 50) -> list[CommandInfo]:
        q = substring.upper()
        out: list[CommandInfo] = []
        for name, cmd in sorted(self._by_name.items()):
            if q in name.upper():
                out.append(cmd)
                if len(out) >= limit:
                    break
        return out

    def recipe(self, key: str) -> dict[str, Any]:
        try:
            return self._manifest["recipes"][key]
        except KeyError as exc:
            raise KeyError(f"Unknown recipe: {key}") from exc

    def recipe_steps(self, key: str, **params: str | int) -> list[str]:
        """Expand a named recipe; `{n}` placeholders are substituted."""
        rec = self.recipe(key)
        steps: list[str] = []
        for step in rec["steps"]:
            s = step
            for k, v in params.items():
                s = s.replace("{" + k + "}", str(v))
            steps.append(s)
        return steps

    def subsystem_guide(self, prefix: str) -> str | None:
        return self._manifest.get("subsystems", {}).get(prefix)

    def help_text(self, name: str) -> str:
        cmd = self.require(name)
        lines = [cmd.name, f"page {cmd.page}", f"usage {cmd.usage}"]
        if cmd.summary:
            lines.append(cmd.summary)
        if cmd.rst_default:
            lines.append(f"*RST {cmd.rst_default}")
        if cmd.parameters:
            lines.append("parameters:")
            lines.extend(f"  {p}" for p in cmd.parameters)
        if cmd.return_values:
            lines.append("returns:")
            lines.extend(f"  {r}" for r in cmd.return_values)
        if cmd.examples:
            lines.append("examples:")
            lines.extend(f"  {e}" for e in cmd.examples)
        return "\n".join(lines)
