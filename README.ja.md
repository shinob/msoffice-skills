# Office File Skills

[English](README.md)

既存の Microsoft Office ファイルを、構造を壊さずに確認・編集・検証するための Codex / Claude 互換スキル集です。

対象は既存ファイルへの安全で限定的な操作です。テキスト編集、Word のデザイン調整、VBA の抽出・編集支援を扱います。新規 Office ファイルの作成は対象外です。

## スキル一覧

| スキル | 対象ファイル | モード | 主な用途 |
|--------|--------------|--------|----------|
| [docx-text-ops](docx-text-ops/SKILL.ja.md) | `.docx` `.docm` `.dotx` `.dotm` | 読み書き | Word 文書のテキスト編集 |
| [docx-design-ops](docx-design-ops/SKILL.ja.md) | `.docx` `.docm` | 読み書き | Word のフォント・色・スタイル・テーマ調整 |
| [pptx-text-ops](pptx-text-ops/SKILL.ja.md) | `.pptx` | 読み書き | PowerPoint のスライド本文・ノート編集 |
| [xlsx-text-ops](xlsx-text-ops/SKILL.ja.md) | `.xlsx` `.xlsm` | 読み書き | Excel ブックのセルテキスト編集 |
| [xlsm-vba-edit](xlsm-vba-edit/SKILL.ja.md) | `.xlsm` | VBE 経由の編集支援 | VBA を書き出し、編集し、Excel VBE で反映 |
| [xlsm-vba-ops](xlsm-vba-ops/SKILL.ja.md) | `.xlsm` | 読み取り専用 | VBA マクロコードの抽出・レビュー |

## どのスキルを使うか

```text
編集したい内容は？
├── .docx / .docm
│   ├── テキスト内容                   -> docx-text-ops
│   └── 見た目・デザイン               -> docx-design-ops
├── .pptx                              -> pptx-text-ops
├── .xlsx / .xlsm
│   ├── セルのテキスト                 -> xlsx-text-ops
│   ├── VBA の修正・機能追加           -> xlsm-vba-edit
│   └── VBA の確認のみ                 -> xlsm-vba-ops
└── 新規ファイル作成                   -> 対象外。python-docx / python-pptx / openpyxl を使用
```

## 共通の安全ルール

1. 編集前に必ず元ファイルをコピーする。
2. 変更前に対象スキルの `extract.py` または検査スクリプトを実行する。
3. テキストのみ・スタイルのみの変更では `.rels` ファイルを編集しない。
4. XML を正規表現だけで書き換えない。正確な編集または名前空間対応の XML ツールを使う。
5. 編集後は抽出・検査スクリプトで必ず検証する。

## 依存関係

| スキル | 依存 |
|--------|------|
| `docx-text-ops` | `pip install python-docx` |
| `docx-design-ops` | デザイン用スクリプトは標準ライブラリのみ。テキスト整合性確認には `python-docx` |
| `pptx-text-ops` | `pip install python-pptx` |
| `xlsx-text-ops` | `pip install openpyxl` |
| `xlsm-vba-edit` / `xlsm-vba-ops` | `pip install oletools` |

## ディレクトリ構成

```text
.
├── README.md
├── README.ja.md
├── LICENSE
├── docx-text-ops/
├── docx-design-ops/
├── pptx-text-ops/
├── xlsx-text-ops/
├── xlsm-vba-edit/
└── xlsm-vba-ops/
```

各スキルディレクトリには以下が含まれます。

```text
SKILL.md       英語の正本
SKILL.ja.md    日本語確認用
scripts/       補助スクリプト
references/    XML 構造・ワークフロー・レシピ
```
