# PPTX Text Structure Reference

## PPTX as a ZIP Package

A `.pptx` file is a ZIP archive. Unpack it to inspect raw XML:

```bash
python skills/pptx-text-ops/scripts/unpack.py presentation.pptx unpacked/
```

Key directories after unpacking:

```
unpacked/
├── ppt/
│   ├── presentation.xml          # slide order (p:sldIdLst)
│   ├── slides/
│   │   ├── slide1.xml            # visible slide content
│   │   ├── slide2.xml
│   │   └── _rels/
│   │       └── slide1.xml.rels   # relationships (images, notes, layouts)
│   ├── notesSlides/
│   │   └── notesSlide1.xml       # speaker notes
│   ├── comments/
│   │   └── comment1.xml          # slide comments
│   ├── charts/
│   │   └── chart1.xml            # chart data and labels
│   ├── slideMasters/
│   │   └── slideMaster1.xml      # master slide (affects all slides)
│   ├── slideLayouts/
│   │   └── slideLayout1.xml      # layout templates
│   └── media/                    # embedded images, videos
├── [Content_Types].xml
└── _rels/
    └── .rels
```

---

## Where Text Lives

### Visible Slide Text

File: `ppt/slides/slideN.xml`

XML path:

```
p:sld
  p:cSld
    p:spTree
      p:sp                    ← shape (text box, title, content placeholder)
        p:txBody
          a:p                 ← paragraph
            a:pPr             ← paragraph properties (alignment, spacing, indent)
            a:r               ← run (inline formatting unit)
              a:rPr           ← run properties (font, size, bold, color)
              a:t             ← actual text content
```

Example:

```xml
<p:sp>
  <p:txBody>
    <a:p>
      <a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="en-US" sz="2400" b="1"/>
        <a:t>Slide Title</a:t>
      </a:r>
    </a:p>
    <a:p>
      <a:r>
        <a:rPr lang="en-US" sz="1800"/>
        <a:t>Body text here.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### Speaker Notes

File: `ppt/notesSlides/notesSlideN.xml`

Same `a:p / a:r / a:t` structure as slides. Notes are independent from visible slide text.

### Comments

File: `ppt/comments/commentN.xml` (older format) or `ppt/comments/comment1.xml` (newer format).

Contains `<p:text>` elements with comment body text.

### Chart Labels

File: `ppt/charts/chartN.xml`

Text appears in `<c:v>`, `<c:f>`, and `<a:t>` elements within chart series data. Chart text may also be backed by an embedded workbook (`ppt/embeddings/`).

### Masters and Layouts

Files: `ppt/slideMasters/slideMasterN.xml`, `ppt/slideLayouts/slideLayoutN.xml`

Same structure as slides. Edits here affect every slide that inherits from the master or layout. Only edit when explicitly instructed.

---

## The Split-Run Problem

A phrase that appears visually as one string may be split across multiple `<a:r>` runs in the XML. This is common when:

- Text was partially formatted (bold, color, font size change mid-phrase)
- Text was edited incrementally in PowerPoint
- Auto-correct or spell-check inserted runs

Example — "Hello World" split across two runs:

```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US" sz="2400"/>
    <a:t>Hello </a:t>
  </a:r>
  <a:r>
    <a:rPr lang="en-US" sz="2400" b="1"/>
    <a:t>World</a:t>
  </a:r>
</a:p>
```

A simple regex search for `Hello World` will find nothing. A naive `<a:t>` replacement will break the text without touching the formatting.

**How to handle split runs:**

- Inspect the full paragraph XML before replacing.
- If formatting should be uniform across the replacement, collapse the runs into one `<a:r>` with the shared `<a:rPr>`.
- If formatting differences must be preserved, replace each run's `<a:t>` separately.
- See [text-edit-recipes.md](text-edit-recipes.md) for patterns.

---

## Namespace Handling

PPTX XML uses multiple namespaces. Key prefixes:

| Prefix | Namespace URI | Used for |
|--------|---------------|----------|
| `p:` | `.../presentationml/2006/main` | Slide structure |
| `a:` | `.../drawingml/2006/main` | Text, shapes, styles |
| `r:` | `.../officeDocument/2006/relationships` | Relationship IDs |
| `c:` | `.../drawingml/2006/chart` | Chart elements |

When parsing XML programmatically, always use namespace-aware tools:

```python
import defusedxml.minidom as minidom

doc = minidom.parse("unpacked/ppt/slides/slide1.xml")
```

Never use regex-only replacement on XML — it will silently corrupt namespace declarations or attributes that contain the target string.

---

## Relationship Files

`.rels` files link slides to their layouts, notes, images, and charts:

```
ppt/slides/_rels/slide1.xml.rels
```

Example:

```xml
<Relationships>
  <Relationship Id="rId1" Type=".../slideLayout" Target="../slideLayouts/slideLayout2.xml"/>
  <Relationship Id="rId2" Type=".../notesSlide" Target="../notesSlides/notesSlide1.xml"/>
  <Relationship Id="rId3" Type=".../image" Target="../media/image1.png"/>
</Relationships>
```

**Never modify `.rels` files for text-only changes.** Changing or removing a relationship ID will break the file.

---

## Smart Quotes in XML

`unpack.py` escapes smart quotes to XML entities so they survive editing. When adding new text with quotes, use XML entities:

| Character | XML Entity |
|-----------|------------|
| `"` (left double) | `&#x201C;` |
| `"` (right double) | `&#x201D;` |
| `'` (left single) | `&#x2018;` |
| `'` (right single / apostrophe) | `&#x2019;` |

`pack.py` re-encodes these to proper Unicode on repack.

---

## Whitespace

Use `xml:space="preserve"` on `<a:t>` elements with leading or trailing spaces:

```xml
<a:t xml:space="preserve"> leading space</a:t>
```

Without this attribute, XML parsers may strip edge whitespace.
