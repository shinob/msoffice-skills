# DOCX デザイン編集レシピ

[English](design-recipes.md)

既存 `.docx` ファイルの見た目を調整するための代表的な手順です。ファイルは `docx-text-ops/scripts/unpack.py` で展開済みである前提です。

## レシピ 1: 本文フォントとサイズを変える

対象: `word/styles.xml`

1. `inspect_design.py` で現在の状態を確認する。
2. `Normal` スタイルと、必要に応じて `w:docDefaults` を更新する。
3. `w:sz` と `w:szCs` は同じ half-point 値にする。
4. 直接書式よりスタイル変更を優先する。

## レシピ 2: 見出しスタイルを変える

対象: `word/styles.xml`

見出しスタイル ID を探し、`w:rPr` と `w:pPr` だけを編集します。`w:basedOn`、`w:next`、アウトラインレベルは保持します。

## レシピ 3: テーマカラーを更新する

対象: `word/theme/theme1.xml`

`w:themeColor` を参照している要素はテーマカラー変更の影響を受けます。直接指定された `w:color w:val` は影響を受けません。

## レシピ 4: テーマフォントを更新する

対象: `word/theme/theme1.xml`

`majorHAnsi` や `minorHAnsi` などテーマ参照を使うスタイルに効きます。直接フォント名が入っているスタイルは `styles.xml` 側で変更します。

## レシピ 5: インライン上書きを扱う

対象: 必要な場合のみ `word/document.xml`

インライン書式はスタイルより優先されます。スタイルで統一したい場合だけ、明示的に direct formatting を除去します。段落スタイル、番号付け、セクションプロパティなど構造要素は削除しません。

## レシピ 6: 表のセル余白を調整する

対象: `word/styles.xml`（テーブルスタイル）

1. 現在のセル余白を確認する。
   ```bash
   python3 docx-design-ops/scripts/inspect_design.py working_copy.docx
   ```
   **TABLE STYLES** セクションで対象スタイルの値を確認します。
   表示がない場合は Word のデフォルト（全辺 108 twips ≈ 1.9 mm）を継承しています。

2. 対象のテーブルスタイル ID を確認する。代表例: `TableGrid`、`TableNormal`。
   ```bash
   grep 'w:type="table"' unpacked/word/styles.xml
   ```

3. spec を作成して適用する。
   ```json
   {
     "styles": {
       "TableGrid": {
         "tblPr": { "cellMarTop": 108, "cellMarLeft": 200, "cellMarBottom": 108, "cellMarRight": 200 }
       }
     }
   }
   ```
   ```bash
   python3 docx-design-ops/scripts/apply_design.py unpacked/ spec.json --dry-run
   python3 docx-design-ops/scripts/apply_design.py unpacked/ spec.json
   ```

値は twips（ポイントの 1/20）で指定します。参考値：

| twips | mm | 備考 |
|-------|----|------|
| 108 | 1.9 | Word デフォルト |
| 160 | 2.8 | やや広め |
| 200 | 3.5 | 読みやすい |
| 360 | 6.4 | 0.25 inch |

特定のセルだけ余白を変えたい場合は `word/document.xml` 内の `<w:tc>` に `w:tcMar` を直接編集してください（`apply_design.py` ではセル個別の上書きには対応していません）。

## 検証

- `inspect_design.py` で意図した変更が見える。
- テキスト抽出結果が変わっていない。
- Word または LibreOffice で開ける。
- `.rels` ファイルを変更していない。
