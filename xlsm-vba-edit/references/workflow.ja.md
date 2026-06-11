# XLSM VBA 編集ワークフロー

[English](workflow.md)

`.xlsm` ブック内の VBA を AI と協力して分析・編集するための手順です。AI は書き出されたテキストファイルを編集し、ユーザーが Excel VBE で反映します。

## 前提

- Python 3.9 以上
- VBE 貼り付け用の Microsoft Excel
- `oletools`

```bash
pip install oletools
```

## 手順

1. バックアップを作成する。
   ```bash
   cp target.xlsm target_backup_YYYYMMDD.xlsm
   ```

2. VBA を書き出す。
   ```bash
   python3 xlsm-vba-edit/scripts/export_vba.py target.xlsm
   ```

3. AI が分析または機能計画を作成する。
   - `{basename}_analysis.md`: バグ・品質レビュー
   - `{basename}_features.md`: 機能追加計画

4. AI が `{basename}_VBA/` 内のファイルを編集する。

5. ユーザーが Excel で `Alt+F11` を押し、変更対象モジュールのコードを置き換えて保存する。

6. 再度 VBA を書き出し、diff で反映内容を確認する。

## トラブルシューティング

| 問題 | 対応 |
|------|------|
| VBE で構文エラーが出る | エラー文を AI に渡して修正する |
| 文字化けする | 再書き出ししてエンコーディングを確認する |
| diff が大きい | VBE の属性行・空白・改行正規化か確認する |
| 動作が想定と違う | 分析に戻り、対象プロシージャを絞る |

## ロールバック

```bash
cp target_backup_YYYYMMDD.xlsm target.xlsm
```
