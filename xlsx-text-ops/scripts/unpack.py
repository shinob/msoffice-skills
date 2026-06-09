"""Unpack an Excel (.xlsx/.xlsm) file into an editable XML directory.

Extracts the ZIP archive and pretty-prints all XML files in-place.

Usage:
    python unpack.py <file.xlsx> <output_dir>

Example:
    python unpack.py workbook.xlsx unpacked/
"""

import argparse
import sys
import zipfile
import xml.dom.minidom
from pathlib import Path

SMART_QUOTE_MAP = {
    "“": "&#x201C;",
    "”": "&#x201D;",
    "‘": "&#x2018;",
    "’": "&#x2019;",
}

XLSX_EXTENSIONS = {".xlsx", ".xlsm"}


def unpack(input_file: str, output_dir: str) -> str:
    src = Path(input_file)
    dst = Path(output_dir)

    if not src.exists():
        return f"Error: {input_file} does not exist"
    if src.suffix.lower() not in XLSX_EXTENSIONS:
        return f"Error: {input_file} must be a .xlsx or .xlsm file"

    try:
        dst.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(dst)

        xml_files = list(dst.rglob("*.xml")) + list(dst.rglob("*.rels"))
        for f in xml_files:
            _pretty_print(f)
            _escape_smart_quotes(f)

        return f"Unpacked {input_file} ({len(xml_files)} XML files)"
    except zipfile.BadZipFile:
        return f"Error: {input_file} is not a valid Excel file"
    except Exception as e:
        return f"Error: {e}"


def _pretty_print(path: Path) -> None:
    try:
        dom = xml.dom.minidom.parseString(path.read_bytes())
        path.write_bytes(dom.toprettyxml(indent="  ", encoding="utf-8"))
    except Exception:
        pass


def _escape_smart_quotes(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
        for char, entity in SMART_QUOTE_MAP.items():
            text = text.replace(char, entity)
        path.write_text(text, encoding="utf-8")
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unpack an Excel file for XML editing")
    parser.add_argument("input_file", help="Excel file to unpack (.xlsx or .xlsm)")
    parser.add_argument("output_dir", help="Output directory")
    args = parser.parse_args()

    msg = unpack(args.input_file, args.output_dir)
    print(msg)
    if "Error" in msg:
        sys.exit(1)
