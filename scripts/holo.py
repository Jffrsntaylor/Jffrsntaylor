"""Rewrite the README footer with the page's own information content.

N is the README's size in bits. A black hole whose Bekenstein-Hawking entropy
equals N bits has a horizon of A / l_p^2 = 4 * N * ln 2 Planck areas.
"""
import math
import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START = "<!-- HOLO:START -->"
END = "<!-- HOLO:END -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def readme_bits(text: str) -> int:
    # Leave the footer out so the number doesn't depend on itself, and count LF
    # line endings so a Windows checkout gives the same answer as CI.
    body = BLOCK.sub("", text.replace("\r\n", "\n"))
    return len(body.encode("utf-8")) * 8


def planck_areas(bits: int) -> float:
    return 4 * bits * math.log(2)


def round_sig(x: float, digits: int = 4) -> int:
    # "About 66,590" reads better than a figure precise to one Planck area.
    return int(round(x, digits - 1 - int(math.floor(math.log10(x)))))


def footer(bits: int) -> str:
    area = round_sig(planck_areas(bits))
    return (
        f"<sub><i>This page holds {bits:,} bits. A black hole storing the same "
        f"information would have a horizon of about {area:,} Planck areas.</i></sub><br>\n"
        "<sub><i>The observable universe has had about 10<sup>90</sup> bits and "
        "10<sup>120</sup> operations to work with (Lloyd, 2002).</i></sub>"
    )


def main() -> None:
    # newline="" keeps the file's own line endings on read and write.
    with open(README, encoding="utf-8", newline="") as f:
        text = f.read()
    block = f"{START}\n{footer(readme_bits(text))}\n{END}"
    updated = BLOCK.sub(lambda _: block, text, count=1)
    if updated != text:
        with open(README, "w", encoding="utf-8", newline="") as f:
            f.write(updated)


if __name__ == "__main__":
    main()
