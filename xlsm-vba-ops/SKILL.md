---
name: xlsm-vba-ops
description: "Use this skill when the user wants to read or review VBA macro code inside an Excel macro-enabled workbook (.xlsm). Triggers include: auditing VBA modules, reviewing macro logic before a seminar or demo, checking which procedures exist, copying VBA source for editing in Claude. This skill is READ-ONLY — it extracts VBA source for inspection. Writing VBA back to the binary requires Excel's VBE; this skill does not support it."
license: Original work, no third-party license constraints
---

# XLSM VBA Operations Skill

Read-only extraction of VBA source code from `.xlsm` files. Output is plain text for reading and reviewing in Claude.

## Quick Reference

| Task | Approach |
|------|----------|
| Extract all VBA modules | `python3 skills/xlsm-vba-ops/scripts/extract.py file.xlsm` |
| List module names only | Extract output → look for `<!-- module: ... -->` lines |
| Review a specific module | Extract → search for the module header |
| Edit VBA code | Extract → edit in Claude → paste into Excel VBE manually |

---

## Non-Goals

- Writing VBA back to the `.xlsm` file — VBA is stored as binary (OLE compound document); writing requires Excel's VBE
- Creating new macros programmatically
- Running or testing macros
- Editing worksheet data or formatting

---

## Core Workflow

1. **Extract** VBA source from the workbook:
   ```bash
   python3 skills/xlsm-vba-ops/scripts/extract.py path/to/file.xlsm
   ```

2. **Read** the output — each module is separated by a `<!-- module: NAME -->` header:
   - `.cls` suffix → class module (ThisWorkbook, Sheet1, etc.)
   - `.bas` suffix → standard module (Module1, Module2, etc.)
   - `.frm` suffix → UserForm module

3. **Review or edit** the extracted source in Claude as plain text.

4. **Apply changes in Excel VBE** — open the workbook, press `Alt+F11`, select the module, paste the updated code.

---

## Output Format

```
<!-- module: ThisWorkbook.cls -->

Attribute VB_Name = "ThisWorkbook"
...

<!-- module: Module1.bas -->

Attribute VB_Name = "Module1"
Public Sub Sample()
    MsgBox "Sample"
End Sub
```

`Attribute VB_Name = ...` lines are internal VBA metadata. The actual user-written code follows.

---

## Dependencies

- `pip install oletools` — VBA extraction (`extract.py` uses `oletools.olevba`)
