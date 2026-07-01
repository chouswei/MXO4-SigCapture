"""Waveform capture over raw SCPI (pattern from R&S RsInstrument MXO examples).

Requires: pip install mxo4-sigcapture[visa] matplotlib
Set MXO4_VISA or MXO4_HOST (socket port 5025).
"""

from __future__ import annotations

import os

from mxo4_sigcapture.scpi import Mxo4Session


def main() -> None:
    resource = os.environ.get("MXO4_VISA")
    host = os.environ.get("MXO4_HOST")

    if resource:
        session = Mxo4Session.from_visa(resource)
    elif host:
        session = Mxo4Session.from_socket(host)
    else:
        raise SystemExit("Set MXO4_VISA or MXO4_HOST")

    with session as mxo:
        print(mxo.identify())
        mxo.write("SYST:DISP:UPD ON")
        mxo.write("AUToscale")
        mxo.opc()
        mxo.write("TRIG:MODE NORM")
        mxo.write("CHAN1:STAT 1")

        mxo.write("FORM:DATA REAL,32")
        mxo.write("FORM:BORD LSBFirst")
        mxo.write("RUNSingle")
        mxo.opc()

        header = mxo.query("CHAN1:DATA:HEAD?")
        print("header:", header)

        # ASCII fallback: binary block parsing needs VISA buffer tuning per site
        mxo.write("FORM:DATA ASC,0")
        raw = mxo.query("CHAN1:DATA?")
        samples = [float(x) for x in raw.split(",") if x.strip()]
        print(f"points: {len(samples)}")

        try:
            import matplotlib.pyplot as plt

            plt.plot(samples)
            plt.title("CH1 waveform (SCPI CHAN1:DATA?)")
            plt.xlabel("sample")
            plt.ylabel("V")
            plt.show()
        except ImportError:
            print("install matplotlib to plot")


if __name__ == "__main__":
    main()
