# DOCX Design Structure Reference

[日本語](docx-design-structure.ja.md)

## Design Files

A `.docx` file is a ZIP package. Design changes usually target:

```text
word/styles.xml            paragraph, character, table, and list styles
word/theme/theme1.xml      theme fonts and color palette
word/document.xml          body content; only touch for explicit inline override cleanup
```

Do not edit `.rels` files for design-only changes.

## Two-Layer Design Model

Word resolves design through two layers:

```text
Layer 1: style and theme definitions
Layer 2: inline direct formatting in document.xml
```

Inline direct formatting wins over style definitions. If a run has a direct red color in `word/document.xml`, changing the heading style color will not affect that run.

## `word/styles.xml`

Important areas:

- `w:docDefaults`: document-wide default run and paragraph properties.
- `w:style`: style definitions for paragraphs, characters, tables, and lists.
- `w:rPr`: run properties such as font, size, color, bold, and italic.
- `w:pPr`: paragraph properties such as spacing, line height, alignment, and indentation.

Critical rule: preserve `w:basedOn` and `w:next`. These define style inheritance and follow-on paragraph behavior.

## `word/theme/theme1.xml`

Important areas:

- `a:fontScheme`: theme major/minor fonts.
- `a:clrScheme`: named theme color slots such as `accent1`, `accent2`, `dk1`, `lt1`, and hyperlink colors.

Theme-referenced styles update automatically when theme slots change. Direct colors and direct font names do not.

## Units

| Property | Unit | Example |
|----------|------|---------|
| `w:sz`, `w:szCs` | half-points | `24` = 12pt |
| `w:spacing w:before`, `w:after` | twentieths of a point | `240` = 12pt |
| `w:spacing w:line` with `auto` | twentieths of a point | `276` = 1.15 line spacing |
| `w:ind w:left`, `w:right` | twentieths of a point | `720` = 0.5 inch |

## Table Cell Margins

Table cell padding is controlled by `w:tblCellMar` inside `w:tblPr`.

**Style-level default** (applies to all cells in tables using that style — edit `word/styles.xml`):

```xml
<w:style w:type="table" w:styleId="TableGrid">
  <w:tblPr>
    <w:tblCellMar>
      <w:top    w:w="108" w:type="dxa"/>
      <w:left   w:w="108" w:type="dxa"/>
      <w:bottom w:w="108" w:type="dxa"/>
      <w:right  w:w="108" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
</w:style>
```

**Table-instance override** (applies to one specific table — edit `word/document.xml`):

```xml
<w:tbl>
  <w:tblPr>
    <w:tblCellMar>
      <w:top    w:w="200" w:type="dxa"/>
      <w:left   w:w="200" w:type="dxa"/>
      <w:bottom w:w="200" w:type="dxa"/>
      <w:right  w:w="200" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
</w:tbl>
```

**Cell-level override** (`w:tcMar` inside `<w:tc>` — edit `word/document.xml`):

```xml
<w:tc>
  <w:tcPr>
    <w:tcMar>
      <w:left  w:w="360" w:type="dxa"/>
      <w:right w:w="360" w:type="dxa"/>
    </w:tcMar>
  </w:tcPr>
</w:tc>
```

`apply_design.py` supports the style-level default only. Table-instance and cell-level edits require direct XML editing.

`w:type="dxa"` means twips (twentieths of a point). Word's built-in default is 108 twips (≈ 1.9 mm) on all sides.

## Namespaces

| Prefix | Namespace |
|--------|-----------|
| `w` | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` |
| `a` | `http://schemas.openxmlformats.org/drawingml/2006/main` |
| `r` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` |
