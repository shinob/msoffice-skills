# XLSM VBA Operations Skill

[English](SKILL.md)

`.xlsm` ファイルから VBA ソースコードを読み取り専用で抽出し、レビューするためのスキルです。

## 使う場面

- VBA モジュール構成を確認したい
- マクロのロジックをレビューしたい
- VBE で修正する前にソースをテキストとして確認したい

## 対象外

- VBA を `.xlsm` に書き戻すこと
- マクロの実行
- 新規マクロの自動作成
- ワークシートデータや書式の編集

## 基本ワークフロー

1. `python3 xlsm-vba-ops/scripts/extract.py target.xlsm` を実行する。
2. 出力内の `<!-- module: NAME -->` 見出しでモジュールを確認する。
3. 必要なモジュールをレビューする。
4. 編集が必要な場合は Excel VBE で手動反映するか、`xlsm-vba-edit` を使う。

詳細は [xlsm-vba-structure.ja.md](references/xlsm-vba-structure.ja.md) を参照してください。
