"""Tests for config apply order and error helper."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from mxo4_sigcapture.capture.setup import apply_all_setup
from mxo4_sigcapture.config.app import AppConfig
from mxo4_sigcapture.scpi.errors import check_error_queue


class MockSession:
    def __init__(self) -> None:
        self.commands: list[str] = []
        self._err_count = 0

    def write(self, command: str) -> None:
        self.commands.append(command)

    def query(self, command: str) -> str:
        self.commands.append(command)
        if command == "*OPC?":
            return "1"
        if command == "ACQuire:SRATe?":
            return "1E+09"
        if command == "ACQuire:POINts?":
            return "100000"
        if command == "ACQuire:POINts:ARATe?":
            return "2.5E+09"
        if command == "TIMebase:SCALe?":
            return "1E-03"
        if command == "SYSTem:ERRor:NEXT?":
            self._err_count += 1
            return '+0,"No error"'
        return ""

    def opc(self) -> str:
        return self.query("*OPC?")

    def stop(self) -> None:
        self.write("STOP")


class ApplyOrderTests(unittest.TestCase):
    def test_apply_order(self) -> None:
        session = MockSession()
        cfg = AppConfig()
        apply_all_setup(session, cfg)
        cmds = session.commands
        stop_idx = cmds.index("STOP")
        ch1_stat = next(i for i, c in enumerate(cmds) if c.startswith("CHANnel1:STATe"))
        acq_type = cmds.index("ACQuire:TYPE SAMPle")
        tim_scal = cmds.index(f"TIMebase:SCALe {cfg.horizontal.time_scale_s_per_div}")
        trig_mode = cmds.index("TRIGger:MODE NORMal")
        form_data = cmds.index("FORMat:DATA REAL,32")
        opc_idx = cmds.index("*OPC?")
        self.assertLess(stop_idx, ch1_stat)
        self.assertLess(ch1_stat, acq_type)
        self.assertLess(acq_type, tim_scal)
        self.assertLess(tim_scal, trig_mode)
        self.assertLess(trig_mode, form_data)
        self.assertLess(form_data, opc_idx)


class ErrorQueueTests(unittest.TestCase):
    def test_drain_no_error(self) -> None:
        session = MagicMock()
        session.query.return_value = '+0,"No error"'
        msgs = check_error_queue(session)
        self.assertEqual(msgs, ['+0,"No error"'])

    def test_drain_with_error(self) -> None:
        session = MagicMock()
        session.query.side_effect = ['-113,"Undefined header"', '+0,"No error"']
        msgs = check_error_queue(session)
        self.assertEqual(len(msgs), 2)


if __name__ == "__main__":
    unittest.main()
