"""
export_vba.py — xlsm ファイルの VBA モジュールをテキストファイルに書き出す

使い方:
    python3 export_vba.py <xlsmファイル>

出力先:
    {元ファイル名}_VBA/
    ├── ExcelObjects/   ThisWorkbook, シートモジュール (.cls)
    ├── Forms/          UserForm (.frm)
    ├── Modules/        標準モジュール (.bas)
    └── Classes/        クラスモジュール (.cls)

依存:
    pip install oletools
"""

import os
import re
import sys


def classify_module(vba_filename: str, vba_code: str) -> str:
    """モジュール種別を判定してサブフォルダ名を返す"""
    ext = os.path.splitext(vba_filename)[1].lower()

    # 標準モジュール（.bas）
    if ext == ".bas":
        return "Modules"

    # UserForm（.frm）
    if ext == ".frm":
        return "Forms"

    # .cls の場合は VB_Base で判定
    match = re.search(r'Attribute VB_Base = "([^"]+)"', vba_code)
    if match:
        vb_base = match.group(1).upper()
        # Workbook (00020819) または Worksheet (00020820) → Excel オブジェクト
        if "00020819" in vb_base or "00020820" in vb_base:
            return "ExcelObjects"
        # UserForm の別表記（念のため）
        if "B4C80393" in vb_base:
            return "Forms"
        # その他の .cls → クラスモジュール
        return "Classes"

    # VB_Base なし・.cls → クラスモジュール
    return "Classes"


def export_vba(xlsm_path: str) -> None:
    try:
        from oletools.olevba import VBA_Parser
    except ImportError:
        print("エラー: oletools がインストールされていません。")
        print("  pip install oletools")
        sys.exit(1)

    if not os.path.isfile(xlsm_path):
        print(f"エラー: ファイルが見つかりません: {xlsm_path}")
        sys.exit(1)

    # 出力ディレクトリ
    basename = os.path.splitext(os.path.basename(xlsm_path))[0]
    out_root = os.path.join(os.path.dirname(xlsm_path), basename + "_VBA")
    subfolders = ["ExcelObjects", "Forms", "Modules", "Classes"]
    for sf in subfolders:
        os.makedirs(os.path.join(out_root, sf), exist_ok=True)

    # VBA 抽出
    vba = VBA_Parser(xlsm_path)
    if not vba.detect_vba_macros():
        print("VBA マクロが見つかりませんでした。")
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

    # サマリー表示
    total = sum(counts.values())
    print(f"出力先: {out_root}/")
    print(f"合計: {total} モジュール")
    for sf in subfolders:
        print(f"  {sf:14s}: {counts[sf]} 件")
    if errors:
        print("\n書き込みエラー:")
        for e in errors:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python3 export_vba.py <xlsmファイル>")
        sys.exit(1)
    export_vba(sys.argv[1])
