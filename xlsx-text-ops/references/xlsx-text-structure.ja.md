# XLSX テキスト構造リファレンス

[English](xlsx-text-structure.md)

## XLSX/XLSM は ZIP パッケージ

`.xlsx` と `.xlsm` は ZIP パッケージです。XML を確認する前に展開します。

```bash
python3 xlsx-text-ops/scripts/unpack.py workbook.xlsx unpacked/
```

主なファイル:

```text
xl/workbook.xml                  シート名、名前定義、ブック情報
xl/sharedStrings.xml             共有文字列テーブル。主な編集対象
xl/worksheets/sheetN.xml         セル、inline string、ヘッダー、フッター
xl/comments/commentN.xml         従来コメント
xl/threadedComments/*.xml        スレッドコメント
xl/charts/chartN.xml             グラフ文字列やキャッシュラベル
```

## 共有文字列

多くのセルテキストは `xl/sharedStrings.xml` に一度だけ保存され、セルは index で参照します。複数セルが同じ index を参照している場合、そのエントリを変えると全セルが同時に変わります。

## inline string

一部のセルは worksheet XML 内に直接テキストを持ちます。

```xml
<c r="B2" t="inlineStr">
  <is><t>インライン文字列</t></is>
</c>
```

これは `sharedStrings.xml` には出ません。

## シート名と名前定義

`xl/workbook.xml` にあります。シート名変更時は `sheetId` と `r:id` を変更しません。

## リレーションシップ

テキストのみの変更では `.rels` ファイルを編集しません。
