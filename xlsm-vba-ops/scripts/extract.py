#!/usr/bin/env python3
"""Extract VBA source code from an .xlsm file."""
import sys
from pathlib import Path
from oletools.olevba import VBA_Parser


def extract(input_file: str) -> str:
    src = Path(input_file)
    if not src.exists():
        raise FileNotFoundError(src)

    vba = VBA_Parser(str(src))
    if not vba.detect_vba_macros():
        return "(VBA macros not found)"

    sections: list[str] = []
    for (_fname, _stream_path, vba_filename, vba_code) in vba.extract_macros():
        sections.append(f"<!-- module: {vba_filename} -->")
        sections.append(vba_code.rstrip())

    return "\n\n".join(sections)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.xlsm>", file=sys.stderr)
        sys.exit(1)
    print(extract(sys.argv[1]))
