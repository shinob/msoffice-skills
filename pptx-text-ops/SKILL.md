---
name: pptx-text-ops
description: "Use this skill when the user wants to inspect or edit text in an existing PowerPoint (.pptx) file without redesigning the deck. Triggers include: replacing or rewriting slide text, proofreading or translating a presentation, normalizing product names or terminology, cleaning up placeholder text (Lorem ipsum, XXXX, template prompts), editing speaker notes, or auditing slide content for duplicates, missing translations, or overflow risk. Use this skill when the existing deck layout, images, masters, and relationships must be preserved. Do NOT use for creating new decks from scratch, redesigning layouts, or live PowerPoint automation — use the pptx skill for those."
license: Original work, no third-party license constraints
---

# PPTX Text Operations Skill

[日本語](SKILL.ja.md)

Text-only editing of existing `.pptx` files. Preserves layout, images, masters, themes, and relationships.

## Quick Reference

| Task | Approach |
|------|----------|
| Extract all slide text | `python3 pptx-text-ops/scripts/extract.py presentation.pptx` |
| Inspect raw XML runs | Unpack → read `ppt/slides/slideN.xml` |
| Edit text | Unpack → edit XML → pack |
| Validate after edit | `python3 pptx-text-ops/scripts/extract.py edited.pptx` |
| Visual spot-check | Convert to PDF → render to images |

---

## Non-Goals

- Creating new decks from scratch → use the `pptx` skill
- Redesigning layouts, colors, or themes → use the `pptx` skill
- Animation authoring
- Chart reconstruction or embedded workbook edits
- Live PowerPoint automation → use a COM/MCP server

---

## Core Workflow

**Always follow this order. Never skip the copy and inspection steps.**

1. **Copy** the source file before any edits:
   ```bash
   cp original.pptx working_copy.pptx
   ```

2. **Extract and read** all text before changing anything:
   ```bash
   python3 pptx-text-ops/scripts/extract.py working_copy.pptx
   ```

3. **Unpack** for XML-level inspection or editing:
   ```bash
   python3 pptx-text-ops/scripts/unpack.py working_copy.pptx unpacked/
   ```

4. **Identify edit surfaces** — determine which surfaces contain the target text:
   - Visible slide text (`ppt/slides/slideN.xml`)
   - Speaker notes (`ppt/notesSlides/notesSlideN.xml`)
   - Comments (`ppt/comments/commentN.xml`)
   - Chart labels (`ppt/charts/chartN.xml`)
   - Masters / layouts — only if explicitly needed

5. **Confirm scope** when the same text appears in multiple surfaces. Ask before editing notes or masters if only slide text was requested.

6. **Edit** XML with the Edit tool. Apply the smallest possible text-only change. See [text-edit-recipes.md](references/text-edit-recipes.md).

7. **Pack**:
   ```bash
   python3 pptx-text-ops/scripts/pack.py unpacked/ edited.pptx
   ```

8. **Validate** — re-extract and compare:
   ```bash
   python3 pptx-text-ops/scripts/extract.py edited.pptx
   ```
   Check: old text gone, new text present, no duplicates, no leftover placeholders.

9. **Visual spot-check** when layout risk exists (long translations, rewrites):
   Open `edited.pptx` in PowerPoint or LibreOffice Impress and check for text overflow or overlap.

---

## Edit Safety Rules

- Preserve all non-text XML.
- Do not delete or renumber relationship IDs (`r:id`, `rId*`).
- Do not edit `.rels` files for text-only changes.
- Use namespace-aware XML parsing for programmatic edits — not regex string replacement.
- Use the Edit tool for targeted changes; do not write throwaway Python scripts.
- Keep replacements close in length when layout preservation matters.
- Flag overflow risk when translated or rewritten text is significantly longer than the original.

Read [pptx-text-structure.md](references/pptx-text-structure.md) for details on the XML structure and why split-run replacement is risky.

---

## Placeholder Detection

After editing, always run:

```bash
python3 pptx-text-ops/scripts/extract.py edited.pptx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder|this.*(slide|page).*layout"
```

If grep returns results, fix them before declaring success.

---

## Validation Checklist

- [ ] Old text is gone
- [ ] Replacement text is present and correct
- [ ] No duplicated passages
- [ ] No leftover placeholder text
- [ ] Notes and comments were not unintentionally changed
- [ ] File opens without errors (pack.py validates on repack)
- [ ] (If layout risk) Visual spot-check shows no overflow or overlap

---

## Dependencies

- `pip install python-pptx` — text extraction (`extract.py`)
- `pptx-text-ops/scripts/unpack.py` — unpack PPTX to XML
- `pptx-text-ops/scripts/pack.py` — repack with validation
