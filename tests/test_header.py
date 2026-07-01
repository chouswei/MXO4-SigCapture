"""Parse waveform header tests."""

import unittest

from mxo4_sigcapture.capture.header import parse_header


class HeaderParserTests(unittest.TestCase):
    def test_parse_four_fields(self) -> None:
        h = parse_header("-1.0E-03,9.0E-03,10000,1")
        self.assertEqual(h.record_length, 10000)
        self.assertEqual(h.vals_per_sample, 1)
        self.assertAlmostEqual(h.x_start_s, -1e-3)

    def test_time_axis_length(self) -> None:
        h = parse_header("0,1,100,1")
        self.assertEqual(len(h.time_axis()), 100)


if __name__ == "__main__":
    unittest.main()
