# PPTX Text Edit Recipes

[日本語](text-edit-recipes.ja.md)

## Recipe 1: Replace Text In One Run

Use when the target text appears inside one `<a:t>` element.

```xml
<a:t>Old title</a:t>
```

Replace only the text node:

```xml
<a:t>New title</a:t>
```

## Recipe 2: Replace Text Split Across Runs

When text is split across multiple `<a:r>` runs, preserve the run structure unless the user accepts formatting simplification.

```xml
<a:r><a:t>Old </a:t></a:r>
<a:r><a:rPr b="1"/><a:t>Title</a:t></a:r>
```

Edit the individual `<a:t>` values while keeping `a:rPr` intact.

## Recipe 3: Speaker Notes

Confirm whether notes are in scope. If they are, edit `ppt/notesSlides/notesSlideN.xml` with the same `<a:t>` rules as slide text.

## Recipe 4: Placeholder Cleanup

Search extracted text:

```bash
python3 pptx-text-ops/scripts/extract.py working_copy.pptx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"
```

Remove or replace each placeholder deliberately. Do not edit layout placeholders unless they are part of the requested change.

## Recipe 5: Translation Pass

1. Extract all slide text and notes.
2. Confirm whether notes, comments, charts, masters, and layouts are in scope.
3. Translate slide XML one file at a time.
4. Keep text length risk visible; translations may overflow shapes.
5. Repack, re-extract, and visually check representative slides.

## Validation Checklist

- Old text is gone.
- New text is present and correct.
- Notes were changed only when intended.
- No placeholders remain.
- The file opens in PowerPoint or LibreOffice Impress.
- Long text does not overflow or overlap.
