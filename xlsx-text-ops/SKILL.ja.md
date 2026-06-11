# XLSX Text Operations Skill

[English](SKILL.md)

既存の `.xlsx` / `.xlsm` ファイルのセルテキストだけを編集するスキルです。数式、書式、グラフ、画像、リレーションシップを保持します。

## 使う場面

- セルテキストの書き換え、翻訳、校正
- シート名や名前定義の変更
- コメントやプレースホルダーの確認
- 既存ブックのレイアウトや数式を維持したい場合

## 対象外

- 新規ブックの作成
- レイアウトやセル書式の再設計
- VBA の読み取り・編集（`xlsm-vba-ops` / `xlsm-vba-edit` を使用）
- 数式や非テキスト値の編集

## 基本ワークフロー

1. 元ファイルをコピーする。
2. `python3 xlsx-text-ops/scripts/extract.py working_copy.xlsx` でテキストと影響範囲を確認する。
3. `python3 xlsx-text-ops/scripts/unpack.py working_copy.xlsx unpacked/` で展開する。
4. 通常は `xl/sharedStrings.xml` を編集する。必要に応じて inline string やシート名も確認する。
5. `python3 xlsx-text-ops/scripts/pack.py unpacked/ edited.xlsx` で再梱包する。
6. `extract.py` と Excel / LibreOffice で検証する。

## 安全ルール

- `sharedStrings.xml` の 1 エントリは複数セルから参照される場合がある。
- 1 セルだけを変える場合は新しい `<si>` を追加し、対象セルの index を更新する。
- `.rels` ファイルは編集しない。
- `<c>` の `t` 属性を不用意に変更しない。

詳細は [xlsx-text-structure.ja.md](references/xlsx-text-structure.ja.md) と [text-edit-recipes.ja.md](references/text-edit-recipes.ja.md) を参照してください。
