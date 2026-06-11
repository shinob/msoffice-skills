---
name: xlsx-text-ops
description: "Use this skill when the user wants to inspect or edit text in an existing Excel (.xlsx or .xlsm) file without redesigning the workbook. Triggers include: replacing or rewriting cell text, proofreading or translating a workbook, normalizing product names or terminology, cleaning up placeholder text (Lorem ipsum, XXXX, template prompts), editing sheet names or named ranges, or auditing cell content for duplicates or missing translations. Use this skill when the existing layout, formulas, formatting, images, and relationships must be preserved. Do NOT use for creating new workbooks from scratch or redesigning layouts — use openpyxl scripting for those. Do NOT use for reading or editing VBA macro code — use the xlsm-vba-ops skill for that."
license: Original work, no third-party license constraints
---

# XLSX Text Operations Skill

[日本語](SKILL.ja.md)

Text-only editing of existing `.xlsx` and `.xlsm` files. Preserves formulas, formatting, charts, images, and relationships.

## Quick Reference

| Task | Approach |
|------|----------|
| Extract all cell text | `python3 xlsx-text-ops/scripts/extract.py workbook.xlsx` |
| Inspect raw XML | Unpack → read `xl/sharedStrings.xml` |
| Edit text | Unpack → edit `xl/sharedStrings.xml` → pack |
| Validate after edit | `python3 xlsx-text-ops/scripts/extract.py edited.xlsx` |
| Visual spot-check | Open in Excel or LibreOffice |

---

## Non-Goals

- Creating new workbooks from scratch → use openpyxl scripting
- Redesigning layouts, cell styles, or chart formats
- Editing formulas or cell values that are not text
- Reading VBA macro code → use the `xlsm-vba-ops` skill
- Editing VBA macro code → use the `xlsm-vba-edit` skill
- Live Excel automation → use a COM/MCP server

---

## Core Workflow

**Always follow this order. Never skip the copy and inspection steps.**

1. **Copy** the source file before any edits:
   ```bash
   cp original.xlsx working_copy.xlsx
   ```

2. **Extract and read** all text before changing anything:
   ```bash
   python3 xlsx-text-ops/scripts/extract.py working_copy.xlsx
   ```

3. **Unpack** for XML-level inspection or editing:
   ```bash
   python3 xlsx-text-ops/scripts/unpack.py working_copy.xlsx unpacked/
   ```

4. **Identify edit surfaces** — determine which surfaces contain the target text:
   - Cell text (usually `xl/sharedStrings.xml`)
   - Inline strings in worksheets (`xl/worksheets/sheetN.xml`)
   - Sheet names (`xl/workbook.xml`)
   - Named ranges (`xl/workbook.xml`)
   - Cell comments (`xl/comments/commentN.xml` + `xl/threadedComments/`)
   - Chart labels (`xl/charts/chartN.xml`)

5. **Confirm scope** when the same text appears in multiple surfaces. Ask before editing named ranges or sheet names if only cell text was requested.

6. **Edit** `xl/sharedStrings.xml` with the Edit tool for most cell text changes. Apply the smallest possible text-only change. See [text-edit-recipes.md](references/text-edit-recipes.md).

   > **WARNING — Shared string editing affects all cells that reference the same index.**
   > Before editing an entry in `sharedStrings.xml`, verify with `extract.py` that the change is
   > appropriate for every cell that uses that string. If only one cell should change, you may
   > need to add a new entry rather than overwriting the shared one.

7. **Pack**:
   ```bash
   python3 xlsx-text-ops/scripts/pack.py unpacked/ edited.xlsx
   ```

8. **Validate** — re-extract and compare:
   ```bash
   python3 xlsx-text-ops/scripts/extract.py edited.xlsx
   ```
   Check: old text gone, new text present, no duplicates, no leftover placeholders.

---

## Edit Safety Rules

- Preserve all non-text XML (formulas, styles, relationships, chart data).
- Do not delete or renumber relationship IDs (`r:id`, `rId*`).
- Do not edit `.rels` files for text-only changes.
- Use namespace-aware XML parsing for programmatic edits — not regex string replacement.
- Use the Edit tool for targeted changes; do not write throwaway Python scripts.
- Keep replacements close in length when layout preservation matters (merged cells, column widths).
- Never change the `t` attribute on `<c>` elements (cell type: `s`=shared string, `str`=formula string, `inlineStr`=inline).

Read [xlsx-text-structure.md](references/xlsx-text-structure.md) for details on the shared strings table and why naive index editing is risky.

---

## Placeholder Detection

After editing, always run:

```bash
python3 xlsx-text-ops/scripts/extract.py edited.xlsx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"
```

If grep returns results, fix them before declaring success.

---

## Validation Checklist

- [ ] Old text is gone
- [ ] Replacement text is present and correct
- [ ] No duplicated passages
- [ ] No leftover placeholder text
- [ ] Comments and named ranges were not unintentionally changed
- [ ] File opens without errors (`python3 -c "import openpyxl; openpyxl.load_workbook('edited.xlsx'); print('OK')"`)
- [ ] Formulas still evaluate correctly (spot-check a few cells)

---

## Dependencies

- `pip install openpyxl` — text extraction and validation (`extract.py`)
- `xlsx-text-ops/scripts/unpack.py` — unpack XLSX to XML
- `xlsx-text-ops/scripts/pack.py` — repack with OPC-correct ordering
