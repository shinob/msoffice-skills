# Text Edit Recipes

Patterns for common text operations on `.docx` files. All recipes assume the file has been unpacked with `unpack.py`.

---

## Recipe 1: Same-String Replacement (Single Run)

Use when the target phrase is contained in a single `<w:t>` element.

**Before editing**, read the paragraph XML and verify the text is not split:

```xml
<w:r>
  <w:rPr><w:lang w:val="ja-JP"/></w:rPr>
  <w:t>旧製品名</w:t>
</w:r>
```

**Edit** with the Edit tool — replace only the `<w:t>` content:

```xml
<w:r>
  <w:rPr><w:lang w:val="ja-JP"/></w:rPr>
  <w:t>新製品名</w:t>
</w:r>
```

**Validate**: run `extract.py` and confirm the old string is gone.

---

## Recipe 2: Replacement Across Split Runs

Use when the target phrase spans multiple runs (see [docx-text-structure.md](docx-text-structure.md) for why this happens).

**Identify** the runs by reading the full `<w:p>` block:

```xml
<w:p>
  <w:r>
    <w:rPr><w:lang w:val="ja-JP"/></w:rPr>
    <w:t xml:space="preserve">旧 </w:t>
  </w:r>
  <w:r>
    <w:rPr><w:b/><w:lang w:val="ja-JP"/></w:rPr>
    <w:t>フレーズ</w:t>
  </w:r>
</w:p>
```

**Option A — Collapse to one run** (when uniform formatting is acceptable):

```xml
<w:p>
  <w:r>
    <w:rPr><w:lang w:val="ja-JP"/></w:rPr>
    <w:t>新フレーズ</w:t>
  </w:r>
</w:p>
```

**Option B — Preserve run formatting** (when formatting differences must be kept):
Distribute the replacement text across runs, keeping each run's `<w:rPr>` intact.

```xml
<w:p>
  <w:r>
    <w:rPr><w:lang w:val="ja-JP"/></w:rPr>
    <w:t xml:space="preserve">新 </w:t>
  </w:r>
  <w:r>
    <w:rPr><w:b/><w:lang w:val="ja-JP"/></w:rPr>
    <w:t>フレーズ</w:t>
  </w:r>
</w:p>
```

---

## Recipe 3: Placeholder Cleanup

Use to remove `Lorem ipsum`, `XXXX`, `TBD`, or template prompt text.

**Find** candidates across all surfaces:

```bash
python3 skills/docx-text-ops/scripts/extract.py working_copy.docx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder"
```

Then unpack and search the XML to locate the exact elements:

```bash
grep -rn "lorem\|xxxx\|TBD" unpacked/word/
```

**After editing**, re-run the grep to confirm all instances are gone:

```bash
python3 skills/docx-text-ops/scripts/extract.py edited.docx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder"
```

---

## Recipe 4: Header or Footer Edit

Headers and footers are in separate XML files. Identify which file to edit:

```bash
ls unpacked/word/header*.xml unpacked/word/footer*.xml
```

Each file uses the same `w:p / w:r / w:t` structure as the body. Edit the `<w:t>` content directly:

```xml
<!-- word/header1.xml -->
<w:p>
  <w:r>
    <w:t>Updated Header Text</w:t>
  </w:r>
</w:p>
```

**Confirm** which header file corresponds to which section by checking `word/_rels/document.xml.rels`.

**Validate** by checking that body text was not changed:

```bash
python3 skills/docx-text-ops/scripts/extract.py edited.docx | grep "\[header\]"
```

---

## Recipe 5: Footnote or Endnote Edit

File: `word/footnotes.xml` or `word/endnotes.xml`

Locate the target footnote by id:

```bash
grep -n 'w:id="3"' unpacked/word/footnotes.xml
```

Edit only the body text run — do not touch the superscript reference number run (identified by `<w:vertAlign w:val="superscript"/>`):

```xml
<w:footnote w:id="3">
  <w:p>
    <w:r>
      <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
      <w:t>3</w:t>             <!-- do not edit this run -->
    </w:r>
    <w:r>
      <w:t xml:space="preserve"> Updated footnote body text.</w:t>
    </w:r>
  </w:p>
</w:footnote>
```

---

## Recipe 6: Terminology Normalization (Glossary-Driven)

Use when standardizing product names, labels, or abbreviations across a document.

**Step 1** — Extract all text and identify all variants:

```bash
python3 skills/docx-text-ops/scripts/extract.py working_copy.docx | grep -i "old term"
```

**Step 2** — Unpack and search all word XML files:

```bash
grep -rn "old term" unpacked/word/
```

**Step 3** — For each occurrence, read the surrounding `<w:p>` block to check for split runs.

**Step 4** — Apply replacements with the Edit tool.

**Step 5** — Validate:

```bash
python3 skills/docx-text-ops/scripts/extract.py edited.docx | grep -i "old term"
```

Zero results = success.

---

## Recipe 7: Translation Pass

Use when translating all document text to another language.

**Before starting:**

- Extract full text with `extract.py` and save as reference.
- Confirm whether headers, footers, and footnotes should also be translated (ask if unclear).
- Estimate length difference — translated text may be 20–40% longer and affect layout.

**Workflow:**

1. Unpack.
2. Process `word/document.xml` section by section: read paragraph → translate `<w:t>` content → edit.
3. For each paragraph, check the run structure first. If runs are split, collapse to single runs before translating (see Recipe 2, Option A) when uniform formatting is acceptable.
4. Repeat for `word/header*.xml`, `word/footer*.xml`, `word/footnotes.xml` if in scope.
5. Pack.
6. Validate — re-extract and compare paragraph count.

**Layout risk check**: open the edited file in Word or LibreOffice to spot text overflow in narrow columns, table cells, or text boxes.

---

## Validation and Risk Checklist

Run after every edit session:

```bash
# 1. Text extraction
python3 skills/docx-text-ops/scripts/extract.py edited.docx

# 2. Placeholder check
python3 skills/docx-text-ops/scripts/extract.py edited.docx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"

# 3. Old strings gone (substitute your actual search term)
python3 skills/docx-text-ops/scripts/extract.py edited.docx | grep -i "old term"

# 4. File integrity
python3 -c "import docx; docx.Document('edited.docx'); print('OK')"
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Regex replace on raw XML | Corrupts namespace declarations and attributes | Use the Edit tool with exact strings |
| Replacing `<w:t>` without checking for split runs | Partial replacement — part of the phrase survives in another run | Read the full `<w:p>` before editing |
| Editing `<w:ins>` or `<w:del>` runs | Corrupt tracked-change state; Word may refuse to open | Ask user to accept/reject all changes first |
| Deleting a relationship ID | File opens with errors or images go missing | Never touch `.rels` files for text changes |
| Missing `xml:space="preserve"` on `<w:t>` with edge spaces | Word strips leading/trailing spaces silently | Add the attribute whenever the text has edge spaces |
| No post-edit validation | Silently broken file shipped | Always run `extract.py` after repacking |
