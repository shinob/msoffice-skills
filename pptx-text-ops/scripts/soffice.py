"""LibreOffice wrapper for headless PPTX-to-PDF conversion.

Locates the soffice binary and runs it with the given arguments.

Usage:
    python soffice.py --headless --convert-to pdf input.pptx
    python soffice.py --headless --convert-to pdf --outdir /tmp input.pptx

Example:
    python soffice.py --headless --convert-to pdf presentation.pptx
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

_SOFFICE_CANDIDATES = [
    "soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/lib/libreoffice/program/soffice",
    "/usr/bin/soffice",
]


def _find_soffice() -> Optional[str]:
    for candidate in _SOFFICE_CANDIDATES:
        if shutil.which(candidate):
            return candidate
        if Path(candidate).is_file():
            return candidate
    return None


def convert(input_file: str, to_format: str, outdir: Optional[str] = None) -> str:
    binary = _find_soffice()
    if not binary:
        return "Error: LibreOffice (soffice) not found. Install LibreOffice to use this command."

    src = Path(input_file)
    if not src.exists():
        return f"Error: {input_file} does not exist"

    cmd = [binary, "--headless", "--convert-to", to_format]
    if outdir:
        cmd += ["--outdir", outdir]
    cmd.append(str(src))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            detail = result.stderr.strip() or "conversion failed"
            return f"Error: {detail}"
        return result.stdout.strip() or f"Converted {input_file} to {to_format}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LibreOffice headless conversion")
    parser.add_argument("input_file", help="File to convert")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--convert-to", required=True, dest="to_format",
                        help="Target format (e.g. pdf)")
    parser.add_argument("--outdir", help="Output directory")
    args = parser.parse_args()

    msg = convert(args.input_file, args.to_format, args.outdir)
    print(msg)
    if "Error" in msg:
        sys.exit(1)
