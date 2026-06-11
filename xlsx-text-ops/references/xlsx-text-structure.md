# XLSX Text Structure Reference

[日本語](xlsx-text-structure.ja.md)

## XLSX/XLSM As ZIP Packages

`.xlsx` and `.xlsm` files are ZIP packages. Unpack before XML-level inspection:

```bash
python3 xlsx-text-ops/scripts/unpack.py workbook.xlsx unpacked/
```

Key files:

```text
xl/workbook.xml                  sheet names, defined names, workbook metadata
xl/sharedStrings.xml             shared string table; primary text edit target
xl/worksheets/sheetN.xml         cells, inline strings, headers, footers
xl/comments/commentN.xml         legacy notes
xl/threadedComments/*.xml        threaded comments
xl/charts/chartN.xml             chart text and cached labels
xl/worksheets/_rels/*.rels       relationships; do not edit for text-only changes
```

## Shared Strings

Excel stores most text once in `xl/sharedStrings.xml`. Worksheet cells reference entries by index:

```xml
<sst>
  <si><t>Product</t></si>
  <si><t>Price</t></si>
</sst>
```

If multiple cells reference the same index, editing that entry changes all of those cells. Verify scope with `extract.py` before editing.

## Inline Strings

Some cells store text directly in worksheet XML:

```xml
<c r="B2" t="inlineStr">
  <is><t>Inline text</t></is>
</c>
```

Inline strings do not appear in `sharedStrings.xml`.

## Formula String Results

Cells with `t="str"` usually contain cached formula output. Do not edit cached `<v>` text as the source of truth; edit the formula only when formula changes are in scope.

## Sheet Names And Defined Names

Sheet names and defined names are in `xl/workbook.xml`. Preserve `sheetId` and `r:id` when renaming sheets.

## Relationships

Do not edit `.rels` files for text-only changes. They connect sheets to charts, comments, drawings, and images.
