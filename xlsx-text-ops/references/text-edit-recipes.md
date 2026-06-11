# XLSX Text Edit Recipes

[日本語](text-edit-recipes.ja.md)

## Recipe 1: Replace A Shared String

Use when the target shared string should change everywhere it is used.

```bash
python3 xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep "Old text"
```

Then edit the matching `<si><t>...</t></si>` entry in `xl/sharedStrings.xml`.

## Recipe 2: Change Only One Cell That Uses A Shared String

If the shared string is used by multiple cells but only one cell should change:

1. Append a new `<si>` entry to `sharedStrings.xml`.
2. Note the new zero-based index.
3. Update the target cell's `<v>` in `xl/worksheets/sheetN.xml` to the new index.
4. Do not renumber existing shared string entries.

## Recipe 3: Rich Text Shared Strings

Rich text entries contain multiple `<r>` runs. Preserve run formatting unless the user accepts flattening the text.

## Recipe 4: Rename A Sheet

Edit only the `name` attribute in `xl/workbook.xml`:

```xml
<sheet name="Sales Data" sheetId="1" r:id="rId1"/>
```

Do not change `sheetId` or `r:id`.

## Recipe 5: Placeholder Cleanup

```bash
python3 xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder"
```

Replace placeholders with final text or an intentionally empty value. Validate after repacking.

## Recipe 6: Translation Pass

1. Extract all text and keep it as a reference.
2. Confirm whether comments, sheet names, and defined names are in scope.
3. Edit `sharedStrings.xml` first, then inline strings if present.
4. Repack and re-extract.
5. Spot-check column widths and merged cells for overflow.

## Validation Checklist

- Old text is gone where intended.
- Shared string changes did not affect unintended cells.
- Comments, sheet names, and defined names changed only when intended.
- The file opens in Excel or LibreOffice.
