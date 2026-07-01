"""Example: catalog-only usage (no instrument required)."""

from mxo4_sigcapture.scpi import ScpiCatalog


def main() -> None:
    cat = ScpiCatalog.load()
    print(cat.connection["hislip"])
    print("commands:", len(cat))
    print(cat.help_text("CHANnel<ch>:STATe"))
    print("recipe reset:", cat.recipe_steps("reset"))
    print("recipe waveform:", cat.recipe_steps("ascii_waveform", n=1))


if __name__ == "__main__":
    main()
