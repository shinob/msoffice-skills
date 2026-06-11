# PPTX Text Structure Reference

[日本語](pptx-text-structure.ja.md)

## PPTX As A ZIP Package

A `.pptx` file is a ZIP package. Unpack it before XML-level inspection:

```bash
python3 pptx-text-ops/scripts/unpack.py presentation.pptx unpacked/
```

Key files:

```text
ppt/slides/slideN.xml              visible slide text
ppt/notesSlides/notesSlideN.xml    speaker notes
ppt/comments/commentN.xml          comments, when present
ppt/charts/chartN.xml              chart labels and cached text
ppt/slideMasters/                  master text; edit only when explicitly needed
ppt/slideLayouts/                  layout text; edit only when explicitly needed
ppt/slides/_rels/*.rels            relationships; do not edit for text-only changes
```

## Text Containers

Visible text usually lives in DrawingML text bodies:

```xml
<a:txBody>
  <a:p>
    <a:r>
      <a:t>Slide text</a:t>
    </a:r>
  </a:p>
</a:txBody>
```

Runs may be split by formatting, hyperlinks, proofing data, or manual edits.

## Speaker Notes

Speaker notes live in `ppt/notesSlides/notesSlideN.xml`. Do not change notes unless the user asks for notes to be included.

## Masters And Layouts

Slide masters and layouts may contain placeholders and inherited text. Edit them only when the requested change is clearly about master/layout text or repeated inherited content.

## Relationships

Do not edit `.rels` files for text-only changes. They connect slides to images, charts, notes, layouts, and other package parts.
