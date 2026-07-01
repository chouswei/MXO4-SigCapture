"""Browse SCPI catalog and recipes (no instrument)."""

from mxo4_sigcapture.scpi import ScpiCatalog


def main() -> None:
    cat = ScpiCatalog.load()
    print(f"{cat.manifest['instrument']}: {len(cat)} commands")
    print(cat.help_text("CHANnel<ch>:STATe"))
    print("recipe single_acquire:", cat.recipe_steps("single_acquire"))
    print("recipe ascii_waveform ch1:", cat.recipe_steps("ascii_waveform", n=1))


if __name__ == "__main__":
    main()
