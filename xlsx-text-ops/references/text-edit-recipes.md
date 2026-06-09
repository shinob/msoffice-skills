# Text Edit Recipes

Patterns for common text operations on `.xlsx` and `.xlsm` files. All recipes assume the
file has been unpacked with `unpack.py`.

---

## Recipe 1: Replace Text in a Shared String (Simple Case)

Use when the target phrase is a plain `<si><t>...</t></si>` entry and the replacement
applies to **every cell** that references it.

**Before editing**, confirm the scope:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep "旧テキスト"
```

If the output shows the string in the expected cells only, proceed.

**Find the index** in `xl/sharedStrings.xml`:

```xml
<si><t>旧テキスト</t></si>      <!-- suppose this is index 3 -->
```

**Edit** with the Edit tool — replace only the `<t>` content:

```xml
<si><t>新テキスト</t></si>
```

**Validate**:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep "旧テキスト"
```

Zero results = success.

---

## Recipe 2: Replace Text in Only One Cell (New Entry Required)

Use when a shared string is referenced by multiple cells but only one cell should change.

**Step 1** — Note the current index of the string in `sharedStrings.xml`.

**Step 2** — Append a **new** `<si>` entry at the end of `sharedStrings.xml`:

```xml
<!-- existing entries -->
<si><t>共通テキスト</t></si>   <!-- index 0, used by many cells -->
...
<!-- new entry added at the end -->
<si><t>このセルだけ変更後</t></si>  <!-- new index N -->
```

**Step 3** — Open the target worksheet file (`xl/worksheets/sheetN.xml`) and update
the `<v>` in the specific cell to the new index:

```xml
<!-- before -->
<c r="B5" t="s"><v>0</v></c>

<!-- after -->
<c r="B5" t="s"><v>N</v></c>
```

**Step 4** — Validate that other cells still show the original text:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep -E "共通テキスト|このセルだけ"
```

---

## Recipe 3: Replace Text in a Rich-Text Shared String

Use when the shared string entry contains multiple `<r>` runs (partial formatting).

**Inspect** the full `<si>` block in `sharedStrings.xml`:

```xml
<si>
  <r>
    <rPr><b/><sz val="12"/><name val="Calibri"/></rPr>
    <t>重要：</t>
  </r>
  <r>
    <rPr><sz val="12"/><name val="Calibri"/></rPr>
    <t xml:space="preserve"> 旧テキスト</t>
  </r>
</si>
```

**Option A — Collapse to one run** (when uniform formatting is acceptable):

```xml
<si>
  <r>
    <rPr><sz val="12"/><name val="Calibri"/></rPr>
    <t>重要： 新テキスト</t>
  </r>
</si>
```

**Option B — Preserve run formatting** (when bold/color differences must be kept):
Replace each `<t>` separately, distributing the new text across the runs.

```xml
<si>
  <r>
    <rPr><b/><sz val="12"/><name val="Calibri"/></rPr>
    <t>重要：</t>
  </r>
  <r>
    <rPr><sz val="12"/><name val="Calibri"/></rPr>
    <t xml:space="preserve"> 新テキスト</t>
  </r>
</si>
```

---

## Recipe 4: Rename a Sheet

File: `xl/workbook.xml`

**Find** the `<sheet>` element:

```xml
<sheet name="Sheet1" sheetId="1" r:id="rId1"/>
```

**Edit** the `name` attribute only:

```xml
<sheet name="売上データ" sheetId="1" r:id="rId1"/>
```

**Do not change** `sheetId` or `r:id`.

**Validate**:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep "\[sheet\]"
```

---

## Recipe 5: Placeholder Cleanup

Use to remove `Lorem ipsum`, `XXXX`, `TBD`, or template prompt text from cells.

**Find** candidates:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder"
```

Note the cell addresses. Unpack and search `xl/sharedStrings.xml` for the exact string.

**Edit** or **remove** the `<si>` entry. If removing, do not renumber remaining entries —
instead replace the content with an empty string or appropriate value:

```xml
<!-- replace placeholder content -->
<si><t></t></si>
```

**After editing**, re-run the grep to confirm all instances are gone.

---

## Recipe 6: Terminology Normalization (Glossary-Driven)

Use when standardizing product names, labels, or abbreviations across a workbook.

**Step 1** — Extract all text and find all variants:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py working_copy.xlsx | grep -i "旧用語"
```

**Step 2** — Unpack and search `sharedStrings.xml` for occurrences:

```bash
grep -n "旧用語" unpacked/xl/sharedStrings.xml
```

**Step 3** — For each occurrence, check the surrounding `<si>` block for split runs.

**Step 4** — Apply replacements with the Edit tool, entry by entry.

**Step 5** — Validate:

```bash
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep -i "旧用語"
```

Zero results = success.

---

## Recipe 7: Edit an Inline String Cell

Use when a cell uses `t="inlineStr"` (text is embedded directly in the worksheet).

**Locate** in the worksheet XML (`xl/worksheets/sheetN.xml`):

```xml
<c r="D4" t="inlineStr">
  <is><t>インラインテキスト</t></is>
</c>
```

**Edit** the `<t>` content directly:

```xml
<c r="D4" t="inlineStr">
  <is><t>変更後テキスト</t></is>
</c>
```

Note: this type of cell does **not** appear in `sharedStrings.xml`.

---

## Recipe 8: Translation Pass

Use when translating all cell text to another language.

**Before starting:**

- Extract full text with `extract.py` and save as reference.
- Confirm whether comments and named ranges should also be translated (ask if unclear).
- Estimate length — translated text may be longer and affect column widths.

**Workflow:**

1. Unpack.
2. Open `xl/sharedStrings.xml` — this is the primary translation file.
3. Process entries one at a time: read `<si>` block → translate `<t>` content → edit.
4. Check for split runs before translating (Recipe 3).
5. Pack.
6. Validate — re-extract and compare entry count.
7. Spot-check column widths: if translated text overflows, column width (`<col width="..."/>` in `sheetN.xml`) may need updating.

---

## Validation and Risk Checklist

Run after every edit session:

```bash
# 1. Text extraction
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx

# 2. Placeholder check
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"

# 3. Old strings gone (substitute your actual search term)
python3 skills/xlsx-text-ops/scripts/extract.py edited.xlsx | grep -i "旧テキスト"

# 4. File integrity
python3 -c "import openpyxl; openpyxl.load_workbook('edited.xlsx'); print('OK')"
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Editing sharedStrings without checking scope | Unintended text changes in other cells | Always run `extract.py` first and grep for all occurrences |
| Renumbering `<si>` entries | All cell references become wrong | Never renumber; only add to the end or edit in-place |
| Regex replace on raw XML | Corrupts namespace declarations | Use the Edit tool with exact strings or namespace-aware parsing |
| Editing `<v>` in a formula cell (`t="str"`) | Cached value is wrong until recalculation | Edit the formula in `<f>`, not the cached `<v>` |
| Changing cell type `t` attribute | File opens with type errors | Never change the `t` attribute |
| Deleting a `.rels` relationship | Images or charts go missing | Never touch `.rels` files for text changes |
| No post-edit validation | Silently broken file shipped | Always run `extract.py` after repacking |
