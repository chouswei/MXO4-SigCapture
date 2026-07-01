# MXO4 SigCapture

Remote control and waveform capture for the **Rohde & Schwarz MXO4** oscilloscope over SCPI (VISA / HiSLIP). Includes a PySide6 GUI, headless capture scripts, and HDF5 export with metadata.

**Repository:** [github.com/chouswei/MXO4-SigCapture](https://github.com/chouswei/MXO4-SigCapture)  
**Latest release:** [v0.2.0](https://github.com/chouswei/MXO4-SigCapture/releases/tag/v0.2.0)

## Features

- **Raw SCPI** — direct `Mxo4Session` writes/queries; no high-level driver required at runtime
- **Structured setup** — channel vertical (scale, offset, coupling, impedance), timebase, acquire, trigger
- **Waveform fetch** — chunked binary read with header parsing and clip detection
- **HDF5 storage** — captures saved under `data/captures/` with config and readback metadata
- **PySide6 GUI** (`mxo4-gui`) — scope-style graticule plot, SRAT/POIN/SCAL readback overlay, four-channel strip
- **SCPI catalogue** — searchable command index and setup recipes (`mxo4-scpi`)

## Requirements

- Python **3.10+**
- R&S **MXO4** on the network (HiSLIP or VISA)
- Optional: [PyVISA](https://pyvisa.readthedocs.io/) for instrument I/O

## Install

From a git checkout:

```powershell
git clone https://github.com/chouswei/MXO4-SigCapture.git
cd MXO4-SigCapture
pip install -e ".[gui,visa]"
```

From a release tag:

```powershell
pip install "mxo4-sigcapture[gui,visa] @ git+https://github.com/chouswei/MXO4-SigCapture.git@v0.2.0"
```

| Extra | Packages | Use |
|-------|----------|-----|
| `visa` | pyvisa, pyvisa-py | Instrument connection |
| `gui` | PySide6, matplotlib, h5py | Desktop app |
| `hdf5` | h5py | HDF5 read/write |
| `plot` | matplotlib | Plot scripts |
| `rs` | RsInstrument | Optional R&S helper (not used at runtime) |
| `dev` | all of the above | Development |

## Quick start — GUI

```powershell
mxo4-gui
```

1. Enter the VISA resource (e.g. `TCPIP0::<host>::hislip0::INSTR`) and connect.
2. Configure channels (On, V/div, offset, coupling, impedance), trigger, and time/acquire.
3. **Apply** sends setup to the scope; **Capture** fetches waveforms and plots them.
4. Captures are written to `data/captures/*.h5`.

## Headless capture

```powershell
python scripts/capture_once.py --resource "TCPIP0::<host>::hislip0::INSTR" --channel 1
```

Add `--json` for a machine-readable summary on stdout.

## Plot a saved capture

```powershell
python scripts/plot_h5.py data/captures/<file>.h5
```

Use `--save out.png` to write a figure without opening a window.

## SCPI catalogue CLI

```powershell
mxo4-scpi count
mxo4-scpi find "CHANnel:SCALe"
mxo4-scpi show "CHANnel<n>:SCALe"
mxo4-scpi recipe channel_vertical -n 1
mxo4-scpi connection
```

## Python API (minimal)

```python
from mxo4_sigcapture import AppConfig, CaptureService, Mxo4Session

cfg = AppConfig()
cfg.channels[0].enabled = True

with Mxo4Session.from_visa("TCPIP0::<host>::hislip0::INSTR") as session:
    svc = CaptureService(session)
    svc.connect(cfg)
    result = svc.capture_once(cfg)
    for w in result.waveforms:
        print(w.channel, len(w.y), "samples")
```

## Project layout

```
src/mxo4_sigcapture/
  apps/gui/          PySide6 GUI
  capture/           Setup, fetch, capture service
  config/            Channel, horizontal, acquire, trigger models
  formatting/        SI unit display helpers
  scpi/              Session, catalogue, recipes
  storage/           HDF5 writer/loader
scripts/             capture_once, plot_h5, SCPI build tools
tests/               Unit tests (setup, header, HDF5)
data/captures/       Output directory (gitignored *.h5)
docs/reference/      MXO4 manual extract and SCPI command index
```

## Tests

```powershell
pip install -e ".[dev]"
python -m pytest tests/ -q
```

## Notes

- **Hardware only** — designed for a real MXO4; there is no instrument simulator.
- **Long-form SCPI** — commands follow the R&S MXO4 programming manual (see `docs/reference/`).
- Captured `.h5` files are excluded from git; only `data/captures/.gitkeep` is tracked.

## Related

Other projects by [@chouswei](https://github.com/chouswei?tab=repositories) include [MemNet](https://github.com/chouswei/MemNet) (LLM working-memory graph) and tooling for SysML v2 modelling.
