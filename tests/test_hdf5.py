"""HDF5 round-trip tests."""

import tempfile
import unittest
from pathlib import Path

import numpy as np

from mxo4_sigcapture.capture.fetch import ChannelWaveform
from mxo4_sigcapture.capture.header import WaveformHeader
from mxo4_sigcapture.capture.service import CaptureResult
from mxo4_sigcapture.config.app import AppConfig
from mxo4_sigcapture.storage.hdf5 import Hdf5Loader, Hdf5Writer


class Hdf5RoundTripTests(unittest.TestCase):
    def test_write_load_shared_time(self) -> None:
        h = WaveformHeader(0.0, 1e-3, 1000, 1)
        t = h.time_axis()
        y = np.sin(t * 1e3).astype(np.float32)
        wf = ChannelWaveform(channel=1, header=h, y=y, time=t)
        result = CaptureResult(waveforms=[wf], idn="TEST,MXO4,0,0", options="")
        cfg = AppConfig()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.h5"
            Hdf5Writer().write(path, cfg, result)
            loaded = Hdf5Loader().load(path)
            self.assertIn(1, loaded.channels)
            np.testing.assert_allclose(loaded.channels[1]["y"], y)
            self.assertEqual(loaded.attrs["t_unit"], "s")


if __name__ == "__main__":
    unittest.main()
