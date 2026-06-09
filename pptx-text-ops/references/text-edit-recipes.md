# Text Edit Recipes

Patterns for common text operations on `.pptx` files. All recipes assume the file has been unpacked with `unpack.py`.

---

## Recipe 1: Same-String Replacement (Single Run)

Use when the target phrase is contained in a single `<a:t>` element.

**Before editing**, read the slide XML and verify the text is not split:

```xml
<a:r>
  <a:rPr lang="en-US" sz="2400"/>
  <a:t>Old Product Name</a:t>
</a:r>
```

**Edit** with the Edit tool — replace only the `<a:t>` content:

```xml
<a:r>
  <a:rPr lang="en-US" sz="2400"/>
  <a:t>New Product Name</a:t>
</a:r>
```

**Validate**: run `extract.py` and confirm the old string is gone.

---

## Recipe 2: Replacement Across Split Runs

Use when the target phrase spans multiple runs (see [pptx-text-structure.md](pptx-text-structure.md) for why this happens).

**Identify** the runs by reading the full `<a:p>` block:

```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US" sz="2400"/>
    <a:t>Old </a:t>
  </a:r>
  <a:r>
    <a:rPr lang="en-US" sz="2400" b="1"/>
    <a:t>Phrase</a:t>
  </a:r>
</a:p>
```

**Option A — Collapse to one run** (when uniform formatting is acceptable):

```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US" sz="2400"/>
    <a:t>New Phrase</a:t>
  </a:r>
</a:p>
```

**Option B — Preserve run formatting** (when formatting differences must be kept):
Distribute the replacement text across runs, keeping each run's `<a:rPr>` intact.

```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US" sz="2400"/>
    <a:t>New </a:t>
  </a:r>
  <a:r>
    <a:rPr lang="en-US" sz="2400" b="1"/>
    <a:t>Phrase</a:t>
  </a:r>
</a:p>
```

---

## Recipe 3: Placeholder Cleanup

Use to remove `Lorem ipsum`, `XXXX`, `TBD`, or template prompt text.

**Find** candidates across all slides:

```bash
python3 skills/pptx-text-ops/scripts/extract.py working_copy.pptx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder|this.*(slide|page)"
```

Note the slide numbers. Then unpack and edit each affected `slideN.xml`.

**After editing**, re-run the grep to confirm all instances are gone:

```bash
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx | grep -iE "lorem|ipsum|xxxx|tbd|placeholder|this.*(slide|page)"
```

---

## Recipe 4: Speaker Notes Edit

Speaker notes are in separate files from slide content.

**Locate** the notes file:

```
unpacked/ppt/notesSlides/notesSlide1.xml
```

Notes use the same `a:p / a:r / a:t` structure as slides. Edit the `<a:t>` content directly.

**Important**: notes files contain a copy of the slide content in a placeholder shape (for rendering). Do not edit that copy — only edit the notes text box (usually the second `<p:sp>` element, identified by `<p:ph type="body"/>`).

**Validate** by checking that slide text was not changed:

```bash
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx
```

---

## Recipe 5: Terminology Normalization (Glossary-Driven)

Use when standardizing product names, labels, or abbreviations across a deck.

**Step 1** — Extract all text and identify all variants:

```bash
python3 skills/pptx-text-ops/scripts/extract.py working_copy.pptx | grep -i "old term"
```

**Step 2** — Unpack and search across all slide XMLs:

```bash
grep -rn "old term" unpacked/ppt/slides/
grep -rn "old term" unpacked/ppt/notesSlides/
```

**Step 3** — For each occurrence, read the surrounding `<a:p>` block to check for split runs.

**Step 4** — Apply replacements with the Edit tool, slide by slide.

**Step 5** — Validate:

```bash
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx | grep -i "old term"
```

Zero results = success.

---

## Recipe 6: Translation Pass

Use when translating all visible slide text to another language.

**Before starting:**

- Extract full text with `extract.py` and save as reference.
- Confirm whether speaker notes should also be translated (ask if unclear).
- Estimate length difference — translated text may be 20–40% longer and cause overflow.

**Workflow:**

1. Unpack.
2. Process slides one at a time: read → translate `<a:t>` content → edit.
3. For each slide, check the run structure first. If runs are split, collapse to single runs before translating (see Recipe 2, Option A).
4. Pack.
5. Validate — re-extract and compare paragraph count.
6. Visual spot-check for overflow (see below).

**Overflow risk check:**

```bash
python skills/pptx-text-ops/scripts/soffice.py --headless --convert-to pdf edited.pptx
pdftoppm -jpeg -r 150 edited.pdf slide
```

Inspect slides where translated text is significantly longer than the original. Look for text cut off at text box boundaries.

---

## Recipe 7: Find and Flag Long Lines

Use to audit for overflow risk before or after edits.

After text extraction, check for suspiciously long lines:

```bash
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx | awk 'length > 120'
```

Lines over ~120 characters in a single `<a:t>` run are candidates for overflow in typical slide layouts. Flag them for visual review.

---

## Validation and Risk Checklist

Run after every edit session:

```bash
# 1. Text extraction
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx

# 2. Placeholder check
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"

# 3. Old strings gone (substitute your actual search term)
python3 skills/pptx-text-ops/scripts/extract.py edited.pptx | grep -i "old term"

# 4. File integrity — open in PowerPoint or verify with python-pptx
python3 -c "from pptx import Presentation; Presentation('edited.pptx'); print('OK')"
```

Visual QA when needed:

```bash
python skills/pptx-text-ops/scripts/soffice.py --headless --convert-to pdf edited.pptx
pdftoppm -jpeg -r 150 edited.pdf slide
```

Check edited slides for:

- Text overflow or cut-off at text box edges
- Overlapping text elements
- Missing bullets
- Wrapped headings colliding with other elements
- Low contrast after font color changes

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Regex replace on raw XML | Corrupts namespace declarations, attributes, and encoded characters | Use namespace-aware XML parsing or the Edit tool with exact strings |
| Replacing `<a:t>` without checking for split runs | Partial replacement — part of the phrase survives in another run | Read the full `<a:p>` before editing |
| Editing a master to change one slide | Unintentionally changes all slides using that master | Only edit `slideN.xml` unless master edit is explicitly needed |
| Deleting a relationship ID | File opens with errors or images go missing | Never touch `.rels` files for text changes |
| Ignoring notes during search | Old term survives in speaker notes | Always grep `notesSlides/` alongside `slides/` |
| No post-edit validation | Silently broken file shipped | Always run `extract.py` after repacking |
