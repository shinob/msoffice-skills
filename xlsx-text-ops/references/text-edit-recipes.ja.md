# XLSX テキスト編集レシピ

[English](text-edit-recipes.md)

## レシピ 1: 共有文字列を置換

対象の共有文字列を使う全セルが変わってよい場合に使います。`extract.py` で影響範囲を確認してから `xl/sharedStrings.xml` を編集します。

## レシピ 2: 1 セルだけ変更

共有文字列が複数セルで使われているが 1 セルだけ変える場合は、新しい `<si>` を末尾に追加し、対象セルの `<v>` を新しい index に変更します。既存 index は振り直しません。

## レシピ 3: rich text

複数の `<r>` run を持つ場合は、書式を保持しながら各 `<t>` を編集します。平坦化する場合は書式が変わる点を確認します。

## レシピ 4: シート名変更

`xl/workbook.xml` の `name` 属性だけを変更します。`sheetId` と `r:id` は変更しません。

## レシピ 5: プレースホルダー削除

```bash
python3 xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder"
```

検出された値を最終テキストまたは意図した空値に置換し、再梱包後に検証します。

## レシピ 6: 翻訳

コメント、シート名、名前定義も対象か確認します。通常は `sharedStrings.xml` を先に処理し、必要に応じて inline string を編集します。

## 検証

- 古いテキストが意図した箇所から消えている。
- 共有文字列変更が意図しないセルに影響していない。
- Excel または LibreOffice で開ける。
