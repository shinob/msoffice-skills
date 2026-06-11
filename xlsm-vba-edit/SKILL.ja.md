# XLSM VBA Edit Skill

[English](SKILL.md)

`.xlsm` ファイル内の VBA を AI と協力して分析・修正・機能追加するためのスキルです。VBA をテキストファイルへ書き出し、AI が編集し、ユーザーが Excel VBE に貼り付けて反映します。

## 使う場面

- VBA のバグを修正したい
- 未完成機能を実装したい
- 新機能を追加したい
- VBA コードをレビューして改善したい

## 対象外

- `.xlsm` バイナリへ VBA を直接書き戻すこと
- マクロの自動実行や自動テスト
- セルデータや書式の編集（`xlsx-text-ops` を使用）
- 読み取り専用レビューのみ（`xlsm-vba-ops` を使用）

## 基本ワークフロー

1. `python3 xlsm-vba-edit/scripts/export_vba.py target.xlsm` で VBA を `{basename}_VBA/` に書き出す。
2. AI が書き出されたファイルを分析し、必要に応じて `_analysis.md` または `_features.md` を作成する。
3. AI が `_VBA/` 内のテキストファイルを編集する。
4. ユーザーが Excel VBE を開き、対象モジュールへ変更後コードを貼り付ける。
5. 再度 `export_vba.py` で書き出し、diff で反映内容を確認する。

詳細は [workflow.ja.md](references/workflow.ja.md) と [vba-edit-recipes.ja.md](references/vba-edit-recipes.ja.md) を参照してください。
