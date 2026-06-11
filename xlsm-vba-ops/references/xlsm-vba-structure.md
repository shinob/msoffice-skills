# XLSM / VBA Internal Structure

[日本語](xlsm-vba-structure.ja.md)

## File Format

An `.xlsm` workbook is an OPC ZIP package like `.xlsx`, with an additional binary VBA project:

```text
Book1.xlsm
├── [Content_Types].xml
├── _rels/.rels
├── xl/
│   ├── workbook.xml
│   ├── worksheets/sheet1.xml
│   ├── vbaProject.bin
│   └── ...
└── docProps/
```

VBA source is not stored as XML. It is stored inside `xl/vbaProject.bin`, an OLE Compound File Binary Format document.

## `vbaProject.bin`

Typical streams include:

| Stream | Meaning |
|--------|---------|
| `VBA/ThisWorkbook` | ThisWorkbook module |
| `VBA/Sheet1` | worksheet module |
| `VBA/Module1` | standard module |
| `VBA/_VBA_PROJECT` | project metadata |
| `VBA/dir` | compressed module directory and attributes |

Module streams contain compiled p-code and compressed source text. `oletools.olevba` reads these streams and extracts the source text.

## Why Write-Back Is Not Supported

Writing VBA back safely requires rebuilding compressed source streams, maintaining OLE structure, and keeping Excel's compiled state consistent. The most reliable write path is Excel VBE, where Excel handles recompilation and project metadata.

## Module Types

| Extension | Type | Example |
|-----------|------|---------|
| `.cls` | class or Excel object module | `ThisWorkbook.cls`, `Sheet1.cls` |
| `.bas` | standard module | `Module1.bas` |
| `.frm` | UserForm | `UserForm1.frm` |
