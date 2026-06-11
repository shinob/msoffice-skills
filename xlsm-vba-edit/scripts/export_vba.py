"""Export VBA modules from an .xlsm workbook to text files.

Usage:
    python3 export_vba.py <file.xlsm>

Output:
    {workbook_stem}_VBA/
    ├── ExcelObjects/   ThisWorkbook and sheet modules (.cls)
    ├── Forms/          UserForms (.frm)
    ├── Modules/        standard modules (.bas)
    └── Classes/        class modules (.cls)

Dependency:
    pip install oletools
"""

import os
import re
import sys


def classify_module(vba_filename: str, vba_code: str) -> str:
    """Return the output subfolder for a VBA module."""
    ext = os.path.splitext(vba_filename)[1].lower()

    # Standard module (.bas)
    if ext == ".bas":
        return "Modules"

    # UserForm (.frm)
    if ext == ".frm":
        return "Forms"

    # Class modules need VB_Base inspection.
    match = re.search(r'Attribute VB_Base = "([^"]+)"', vba_code)
    if match:
        vb_base = match.group(1).upper()
        # Workbook (00020819) or Worksheet (00020820)
        if "00020819" in vb_base or "00020820" in vb_base:
            return "ExcelObjects"
        # Some UserForms appear as .cls with this base GUID.
        if "B4C80393" in vb_base:
            return "Forms"
        # Other .cls modules are class modules.
        return "Classes"

    # .cls without VB_Base is treated as a class module.
    return "Classes"


def export_vba(xlsm_path: str) -> None:
    try:
        from oletools.olevba import VBA_Parser
    except ImportError:
        print("Error: oletools is not installed.")
        print("  pip install oletools")
        sys.exit(1)

    if not os.path.isfile(xlsm_path):
        print(f"Error: file not found: {xlsm_path}")
        sys.exit(1)

    # Output directory
    basename = os.path.splitext(os.path.basename(xlsm_path))[0]
    out_root = os.path.join(os.path.dirname(xlsm_path), basename + "_VBA")
    subfolders = ["ExcelObjects", "Forms", "Modules", "Classes"]
    for sf in subfolders:
        os.makedirs(os.path.join(out_root, sf), exist_ok=True)

    # VBA extraction
    vba = VBA_Parser(xlsm_path)
    if not vba.detect_vba_macros():
        print("No VBA macros found.")
        return

    counts = {sf: 0 for sf in subfolders}
    errors = []

    for _, _, vba_filename, vba_code in vba.extract_macros():
        if not vba_filename or not vba_code.strip():
            continue

        subfolder = classify_module(vba_filename, vba_code)
        out_path = os.path.join(out_root, subfolder, vba_filename)

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(vba_code)
            counts[subfolder] += 1
        except OSError as e:
            errors.append(f"  {vba_filename}: {e}")

    # Summary
    total = sum(counts.values())
    print(f"Output directory: {out_root}/")
    print(f"Total modules: {total}")
    for sf in subfolders:
        print(f"  {sf:14s}: {counts[sf]}")
    if errors:
        print("\nWrite errors:")
        for e in errors:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 export_vba.py <file.xlsm>")
        sys.exit(1)
    export_vba(sys.argv[1])
