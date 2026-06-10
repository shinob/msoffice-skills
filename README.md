# Office File Skills

Claude Code スキル集。既存の Office ファイルに対してテキストの抽出・編集・検証を行う。
レイアウト・スタイル・画像・数式・リレーションシップはすべて保持したまま、テキストのみを安全に操作する。

---

## スキル一覧

| スキル | 対象ファイル | 読み書き | 主な用途 |
|--------|------------|---------|---------|
| [docx-text-ops](#docx-text-ops) | `.docx` `.docm` `.dotx` | 読み書き | Word 文書のテキスト編集 |
| [pptx-text-ops](#pptx-text-ops) | `.pptx` | 読み書き | PowerPoint スライドのテキスト編集 |
| [xlsx-text-ops](#xlsx-text-ops) | `.xlsx` `.xlsm` | 読み書き | Excel ワークブックのテキスト編集 |
| [xlsm-vba-edit](#xlsm-vba-edit) | `.xlsm` | 読み書き（VBE経由） | Excel VBA の分析・修正・機能追加 |
| [xlsm-vba-ops](#xlsm-vba-ops) | `.xlsm` | **読み取り専用** | Excel VBA マクロの抽出・レビュー |

---

## どのスキルを使うか

```
編集したいファイルは？
├── .docx / .docm → docx-text-ops
├── .pptx         → pptx-text-ops
├── .xlsx / .xlsm
│   ├── セルのテキストを編集したい     → xlsx-text-ops
│   ├── VBA を修正・機能追加したい     → xlsm-vba-edit
│   └── VBA マクロを読むだけでよい    → xlsm-vba-ops
└── 新規ファイルを作りたい → スキル対象外（python-docx / openpyxl スクリプトを使う）
```

---

## 各スキルの詳細

### docx-text-ops

Word 文書（`.docx`）のテキストのみを編集する。スタイル・画像・テーブル・ナンバリング・リレーションシップを保持。

**トリガー例**: 本文の書き換え、翻訳、用語統一、ヘッダー/フッター編集、脚注編集、プレースホルダー除去

**対象外**: ゼロからの文書作成、スタイル再設計、変更履歴（トラックチェンジ）が有効な文書

```bash
# テキスト抽出
python3 skills/docx-text-ops/scripts/extract.py document.docx

# XML展開 → 編集 → 再梱包
python3 skills/docx-text-ops/scripts/unpack.py working_copy.docx unpacked/
# … Edit ツールで word/document.xml を編集 …
python3 skills/docx-text-ops/scripts/pack.py unpacked/ edited.docx
```

依存: `pip install python-docx`

---

### pptx-text-ops

PowerPoint ファイル（`.pptx`）のテキストのみを編集する。レイアウト・画像・マスター・テーマ・リレーションシップを保持。

**トリガー例**: スライドテキストの書き換え、翻訳、用語統一、スピーカーノート編集、プレースホルダー除去

**対象外**: ゼロからのデッキ作成、レイアウト・配色の再設計、アニメーション編集

```bash
# テキスト抽出
python3 skills/pptx-text-ops/scripts/extract.py presentation.pptx

# XML展開 → 編集 → 再梱包
python3 skills/pptx-text-ops/scripts/unpack.py working_copy.pptx unpacked/
# … Edit ツールで ppt/slides/slideN.xml を編集 …
python3 skills/pptx-text-ops/scripts/pack.py unpacked/ edited.pptx
```

依存: `pip install python-pptx`

---

### xlsx-text-ops

Excel ワークブック（`.xlsx` / `.xlsm`）のセルテキストのみを編集する。数式・書式・チャート・画像・リレーションシップを保持。

**トリガー例**: セルテキストの書き換え、翻訳、用語統一、シート名変更、プレースホルダー除去

**対象外**: ゼロからのワークブック作成、レイアウト再設計、VBA 編集（→ xlsm-vba-edit）、VBA 読み取り専用（→ xlsm-vba-ops）

```bash
# テキスト抽出
python3 skills/xlsx-text-ops/scripts/extract.py workbook.xlsx

# XML展開 → 編集 → 再梱包
python3 skills/xlsx-text-ops/scripts/unpack.py working_copy.xlsx unpacked/
# … Edit ツールで xl/sharedStrings.xml を編集 …
python3 skills/xlsx-text-ops/scripts/pack.py unpacked/ edited.xlsx
```

依存: `pip install openpyxl`

> **注意**: `sharedStrings.xml` の1エントリを変更すると、そのインデックスを参照するすべてのセルに影響する。編集前に `extract.py` で影響範囲を確認すること。

---

### xlsm-vba-edit

`.xlsm` ファイルの VBA を AI と協力して分析・修正・機能追加する。VBA をテキストファイルに書き出し、AI が編集し、ユーザーが VBE に貼り付けて反映する。

**トリガー例**: VBA のバグを修正したい、未完成機能を実装したい、新機能を追加したい、VBA コードをレビューして改善したい

**対象外**: セルテキストの編集（→ xlsx-text-ops）、VBA の読み取りのみ（→ xlsm-vba-ops）

```bash
# VBA を分類フォルダに書き出す
python3 skills/xlsm-vba-edit/scripts/export_vba.py file.xlsm
# → file_VBA/{ExcelObjects,Forms,Modules,Classes}/ に出力
```

依存: `pip install oletools`

---

### xlsm-vba-ops

`.xlsm` ファイルから VBA ソースコードを抽出してレビューする。**書き込みは行わない**。

**トリガー例**: VBA モジュールの監査、マクロロジックのレビュー、コードを Claude で確認してから VBE で修正

**対象外**: VBA の書き戻し（バイナリ形式のため Excel VBE が必要）、マクロの実行、ワークシートデータの編集

```bash
# VBA 全モジュールを抽出
python3 skills/xlsm-vba-ops/scripts/extract.py file.xlsm
```

依存: `pip install oletools`

---

## 共通の安全ルール

すべてのスキルに共通する原則：

1. **編集前に必ずコピーを作る** — 元ファイルは変更しない
2. **extract.py で内容を確認してから編集する** — 何が変わるかを把握してから手を入れる
3. **`.rels` ファイルは触らない** — テキスト変更でリレーションシップを編集する必要はない
4. **XML を正規表現で直接置換しない** — 名前空間宣言を破壊する。Edit ツールで正確な文字列を指定する
5. **編集後は必ず extract.py で検証する** — 古いテキストが消えたか、新しいテキストが正しいか確認する

---

## ディレクトリ構造

```
skills/
├── README.md                        このファイル
├── docx-text-ops/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract.py
│   │   ├── unpack.py
│   │   └── pack.py
│   └── references/
│       ├── docx-text-structure.md
│       └── text-edit-recipes.md
├── pptx-text-ops/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract.py
│   │   ├── unpack.py
│   │   └── pack.py
│   └── references/
│       ├── pptx-text-structure.md
│       └── text-edit-recipes.md
├── xlsx-text-ops/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract.py
│   │   ├── unpack.py
│   │   └── pack.py
│   └── references/
│       ├── xlsx-text-structure.md
│       └── text-edit-recipes.md
├── xlsm-vba-edit/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── export_vba.py
│   └── references/
│       ├── workflow.md
│       └── vba-edit-recipes.md
└── xlsm-vba-ops/
    ├── SKILL.md
    ├── scripts/
    │   └── extract.py
    └── references/
        └── xlsm-vba-structure.md
```
