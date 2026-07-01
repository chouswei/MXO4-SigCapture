"""Connect to MXO4 using raw SCPI strings (PyVISA HiSLIP)."""

from __future__ import annotations

import os

from mxo4_sigcapture.scpi import Mxo4Session


def main() -> None:
    resource = os.environ.get("MXO4_VISA", "TCPIP::192.1.2.3::hislip0::INSTR")

    with Mxo4Session.from_visa(resource) as mxo:
        print(mxo.identify())

        for step in mxo.cat.recipe_steps("reset"):
            if step.endswith("?"):
                print(step, "->", mxo.query(step))
            else:
                mxo.write(step)

        # Raw SCPI (short forms from manual examples)
        mxo.write("SYST:DISP:UPD ON")
        mxo.write("TRIG:MODE AUTO")
        mxo.write("CHAN1:STAT 1")
        mxo.write("AUToscale")
        mxo.opc()

        mxo.write("ACQuire:COUNt 1")
        mxo.write("RUNSingle")
        mxo.opc()

        mxo.write("FORM:DATA ASC,0")
        header = mxo.query("CHAN1:DATA:HEAD?")
        values = mxo.query("CHAN1:DATA?")
        print("header:", header)
        print("samples:", len(values.split(",")) if values else 0)

        print(mxo.cat.help_text("CHANnel<ch>:STATe"))


if __name__ == "__main__":
    main()
