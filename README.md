# Office File Skills

[日本語](README.ja.md)

Codex/Claude-compatible skills for inspecting, editing, and validating existing Microsoft Office files while preserving document structure.

These skills focus on safe, narrow operations: text edits, Word design adjustments, and VBA extraction/editing workflows. They are intended for existing files, not for creating new Office documents from scratch.

## Skills

| Skill | Files | Mode | Main use |
|-------|-------|------|----------|
| [docx-text-ops](docx-text-ops/SKILL.md) | `.docx` `.docm` `.dotx` `.dotm` | read/write | Edit Word document text |
| [docx-design-ops](docx-design-ops/SKILL.md) | `.docx` `.docm` | read/write | Adjust Word fonts, colors, styles, and theme |
| [pptx-text-ops](pptx-text-ops/SKILL.md) | `.pptx` | read/write | Edit PowerPoint slide text and speaker notes |
| [xlsx-text-ops](xlsx-text-ops/SKILL.md) | `.xlsx` `.xlsm` | read/write | Edit Excel workbook text |
| [xlsm-vba-edit](xlsm-vba-edit/SKILL.md) | `.xlsm` | assisted write via VBE | Export, edit, and reapply VBA code manually through Excel VBE |
| [xlsm-vba-ops](xlsm-vba-ops/SKILL.md) | `.xlsm` | read-only | Extract and review VBA macro code |

## Which Skill To Use

```text
What do you need to edit?
├── .docx / .docm
│   ├── Text content                    -> docx-text-ops
│   └── Visual design                   -> docx-design-ops
├── .pptx                               -> pptx-text-ops
├── .xlsx / .xlsm
│   ├── Cell text                       -> xlsx-text-ops
│   ├── VBA bug fixes or new features   -> xlsm-vba-edit
│   └── VBA review only                 -> xlsm-vba-ops
└── New file generation                 -> out of scope; use python-docx, python-pptx, or openpyxl scripts
```

## Quick Examples

### Word Text

```bash
python3 docx-text-ops/scripts/extract.py document.docx
python3 docx-text-ops/scripts/unpack.py working_copy.docx unpacked/
# Edit word/document.xml
python3 docx-text-ops/scripts/pack.py unpacked/ edited.docx
```

### Word Design

```bash
python3 docx-design-ops/scripts/inspect_design.py document.docx
python3 docx-text-ops/scripts/unpack.py working_copy.docx unpacked/
python3 docx-design-ops/scripts/apply_design.py unpacked/ spec.json --dry-run
python3 docx-design-ops/scripts/apply_design.py unpacked/ spec.json
python3 docx-text-ops/scripts/pack.py unpacked/ edited.docx
```

### PowerPoint Text

```bash
python3 pptx-text-ops/scripts/extract.py presentation.pptx
python3 pptx-text-ops/scripts/unpack.py working_copy.pptx unpacked/
# Edit ppt/slides/slideN.xml or ppt/notesSlides/notesSlideN.xml
python3 pptx-text-ops/scripts/pack.py unpacked/ edited.pptx
```

### Excel Text

```bash
python3 xlsx-text-ops/scripts/extract.py workbook.xlsx
python3 xlsx-text-ops/scripts/unpack.py working_copy.xlsx unpacked/
# Edit xl/sharedStrings.xml or inline string cells
python3 xlsx-text-ops/scripts/pack.py unpacked/ edited.xlsx
```

### VBA

```bash
python3 xlsm-vba-edit/scripts/export_vba.py workbook.xlsm
python3 xlsm-vba-ops/scripts/extract.py workbook.xlsm
```

## Common Safety Rules

1. Always copy the source file before editing.
2. Run the relevant `extract.py` or inspection script before changing anything.
3. Do not edit `.rels` files for text-only or style-only changes.
4. Do not use regex-only XML rewrites; use exact edits or namespace-aware XML tools.
5. Validate after editing by extracting or inspecting the edited file.

## Dependencies

| Skill | Dependency |
|-------|------------|
| `docx-text-ops` | `pip install python-docx` |
| `docx-design-ops` | standard library for design scripts; `python-docx` for text integrity checks |
| `pptx-text-ops` | `pip install python-pptx` |
| `xlsx-text-ops` | `pip install openpyxl` |
| `xlsm-vba-edit` / `xlsm-vba-ops` | `pip install oletools` |

## Repository Layout

```text
.
├── README.md
├── README.ja.md
├── LICENSE
├── docx-text-ops/
├── docx-design-ops/
├── pptx-text-ops/
├── xlsx-text-ops/
├── xlsm-vba-edit/
└── xlsm-vba-ops/
```

Each skill directory contains:

```text
SKILL.md       English canonical skill instructions
SKILL.ja.md    Japanese review copy
scripts/       Helper scripts
references/    XML/workflow references and recipes
```
