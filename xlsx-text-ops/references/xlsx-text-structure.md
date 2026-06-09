# XLSX Text Structure Reference

## XLSX as a ZIP Package

An `.xlsx` (or `.xlsm`) file is a ZIP archive. Unpack it to inspect raw XML:

```bash
python3 skills/xlsx-text-ops/scripts/unpack.py workbook.xlsx unpacked/
```

Key files after unpacking:

```
unpacked/
├── xl/
│   ├── workbook.xml              # sheet list, named ranges, workbook settings
│   ├── sharedStrings.xml         # ALL cell text (most edits happen here)
│   ├── styles.xml                # cell formatting (do not edit for text changes)
│   ├── worksheets/
│   │   ├── sheet1.xml            # cell data for Sheet1 (references sharedStrings)
│   │   ├── sheet2.xml
│   │   └── _rels/
│   │       └── sheet1.xml.rels   # relationships (charts, images, comments)
│   ├── charts/
│   │   └── chart1.xml            # chart data and axis labels
│   ├── comments/
│   │   └── comment1.xml          # legacy cell comments (Excel notes)
│   ├── threadedComments/
│   │   └── threadedComment1.xml  # modern threaded comments
│   ├── drawings/
│   │   └── drawing1.xml          # shapes, text boxes
│   └── media/                    # embedded images
├── [Content_Types].xml
└── _rels/
    └── .rels
```

---

## The Shared Strings Table — Primary Edit Target

File: `xl/sharedStrings.xml`

Excel stores all cell text **once** in a shared string table to save space. Each worksheet cell
that contains text holds an **index** (integer) pointing to an entry in this table.

```xml
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
     count="5" uniqueCount="3">
  <si><t>製品名</t></si>          <!-- index 0 -->
  <si><t>単価</t></si>            <!-- index 1 -->
  <si><t xml:space="preserve">Hello World </t></si>  <!-- index 2 -->
</sst>
```

`count` = total references across the workbook; `uniqueCount` = entries in this table.
**You do not need to update these numbers** — Excel recalculates them on open.

### Critical: One Edit Affects All Cells Using That Index

If index 0 (`製品名`) is referenced by cells A1 on Sheet1, A1 on Sheet2, and B3 on Sheet3,
editing that entry changes **all three cells simultaneously**. Always verify with `extract.py`
that the change is appropriate everywhere before editing.

If only one cell should change, you must:
1. Add a **new** `<si>` entry at the end of `sharedStrings.xml`.
2. Update the `<v>` in the specific worksheet cell to point to the new index.
3. Optionally remove the old entry only if no other cell references it.

---

## Cell Structure in Worksheets

File: `xl/worksheets/sheetN.xml`

```xml
<sheetData>
  <row r="1">
    <!-- Shared string reference: t="s", <v> holds the index -->
    <c r="A1" t="s">
      <v>0</v>
    </c>

    <!-- Inline string: t="inlineStr", text is embedded directly -->
    <c r="B1" t="inlineStr">
      <is><t>直接テキスト</t></is>
    </c>

    <!-- Formula that returns a string: t="str" -->
    <c r="C1" t="str">
      <f>CONCATENATE(A1," ",B1)</f>
      <v>製品名 直接テキスト</v>
    </c>

    <!-- Numeric cell (no t attribute or t="n"): do not edit as text -->
    <c r="D1">
      <v>12345</v>
    </c>
  </row>
</sheetData>
```

| Cell type (`t`) | Where text lives | Edit target |
|-----------------|-----------------|-------------|
| `s` (shared string) | `xl/sharedStrings.xml` | Edit `<si>` entry by index |
| `inlineStr` | `xl/worksheets/sheetN.xml` | Edit `<is><t>` directly |
| `str` (formula result) | Worksheet `<v>` (cached) | Edit the formula in `<f>`, not `<v>` |
| *(none / `n`)* | Numeric — not text | Do not edit |

**Most text edits target `sharedStrings.xml`.** Inline strings (`inlineStr`) are rare in
typical workbooks but appear when text was added programmatically.

---

## Rich Text in Shared Strings (Split-Run Problem)

Just like PPTX, a single visible string may be stored as multiple `<r>` (run) elements
with different formatting per run:

```xml
<si>
  <r>
    <rPr><b/><sz val="12"/><name val="Calibri"/></rPr>
    <t>重要：</t>
  </r>
  <r>
    <rPr><sz val="12"/><name val="Calibri"/></rPr>
    <t xml:space="preserve"> 本文テキスト</t>
  </r>
</si>
```

A search for `重要： 本文テキスト` in the XML will find nothing. Replace each `<t>` separately,
or collapse to a single `<r>` when uniform formatting is acceptable.

A plain `<si>` with no runs uses `<t>` directly:
```xml
<si><t>Plain text</t></si>
```

---

## Sheet Names and Named Ranges

File: `xl/workbook.xml`

```xml
<!-- Sheet names -->
<sheets>
  <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  <sheet name="売上データ" sheetId="2" r:id="rId2"/>
</sheets>

<!-- Named ranges (defined names) -->
<definedNames>
  <definedName name="売上合計">Sheet1!$B$10</definedName>
  <definedName name="製品リスト">売上データ!$A$2:$A$50</definedName>
</definedNames>
```

Editing sheet `name` attributes here renames the sheet everywhere in the workbook.
Named range `name` attributes can also be changed here.

---

## Cell Comments

Legacy comments (yellow sticky notes) — File: `xl/comments/commentN.xml`

```xml
<commentList>
  <comment ref="B2" authorId="0">
    <text>
      <r><rPr><b/></rPr><t>Author: </t></r>
      <r><t>This cell needs review.</t></r>
    </text>
  </comment>
</commentList>
```

Modern threaded comments — File: `xl/threadedComments/threadedCommentN.xml`

```xml
<threadedComments>
  <threadedComment ref="C3" ...>
    <text>Review this value before submission.</text>
  </threadedComment>
</threadedComments>
```

---

## Headers and Footers

File: `xl/worksheets/sheetN.xml`

```xml
<headerFooter>
  <oddHeader>&amp;C&amp;B岡山県産業振興財団</oddHeader>
  <oddFooter>&amp;L&amp;D&amp;R&amp;P / &amp;N</oddFooter>
</headerFooter>
```

`&C` = center, `&L` = left, `&R` = right, `&B` = bold, `&D` = date, `&P` = page number.
Text content between format codes is editable.

---

## Namespace Handling

XLSX XML uses a single primary namespace for spreadsheet content:

| Prefix | Namespace URI | Used for |
|--------|---------------|----------|
| *(default)* | `http://schemas.openxmlformats.org/spreadsheetml/2006/main` | Workbook, sheets, shared strings |
| `r:` | `.../officeDocument/2006/relationships` | Relationship IDs |
| `a:` | `.../drawingml/2006/main` | Drawing, shapes, text boxes |

When parsing programmatically, always use namespace-aware tools. Never use regex-only
replacement on XML — it silently corrupts namespace declarations.

---

## Relationship Files

`.rels` files link worksheets to their charts, images, and comments:

```
xl/worksheets/_rels/sheet1.xml.rels
```

```xml
<Relationships>
  <Relationship Id="rId1" Type=".../chart" Target="../charts/chart1.xml"/>
  <Relationship Id="rId2" Type=".../comments" Target="../comments/comment1.xml"/>
  <Relationship Id="rId3" Type=".../image" Target="../media/image1.png"/>
</Relationships>
```

**Never modify `.rels` files for text-only changes.**

---

## Whitespace

Use `xml:space="preserve"` on `<t>` elements with leading or trailing spaces:

```xml
<t xml:space="preserve"> leading space</t>
```

Without this attribute, XML parsers strip edge whitespace, breaking the text silently.
