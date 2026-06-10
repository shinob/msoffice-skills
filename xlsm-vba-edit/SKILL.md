---
name: xlsm-vba-edit
description: "Use this skill when the user wants to analyse, fix bugs in, or add
  features to VBA code inside an Excel macro-enabled workbook (.xlsm). Triggers:
  VBA のバグを直したい, VBA に機能を追加したい, xlsm を AI と一緒に修正したい,
  VBA コードを修正して反映したい. Workflow: export VBA to organised text files with
  export_vba.py → AI edits the text files → user pastes into Excel VBE.
  For read-only VBA review without editing, use xlsm-vba-ops instead."
license: Original work, no third-party license constraints
---

# XLSM VBA Edit Skill

AI-assisted workflow for analysing, fixing, and extending VBA code in `.xlsm` files.
VBA is exported to text files, edited by AI, and pasted back via Excel VBE.

## Quick Reference

| Task | Approach |
|------|----------|
| Export VBA to text files | `python3 skills/xlsm-vba-edit/scripts/export_vba.py file.xlsm` |
| Analyse bugs / issues | Run export → use analysis prompt in `references/vba-edit-recipes.md` |
| Plan a new feature | Run export → use feature prompt in `references/vba-edit-recipes.md` |
| Apply fixes to xlsm | AI edits `_VBA/` files → user pastes each module into Excel VBE |

---

## Non-Goals

- Writing VBA directly back to the `.xlsm` binary — VBA is stored as OLE compound document; writing requires Excel's VBE
- Running or testing macros programmatically
- Editing worksheet cell data or formatting (→ use `xlsx-text-ops`)
- Read-only VBA review without editing (→ use `xlsm-vba-ops`)

---

## Core Workflow

1. **Export** VBA source to organised text files:
   ```bash
   python3 skills/xlsm-vba-edit/scripts/export_vba.py path/to/file.xlsm
   ```
   Output: `{basename}_VBA/{ExcelObjects,Forms,Modules,Classes}/`

2. **Analyse or plan** — AI reads the exported files and produces `_analysis.md` (bugs) or `_features.md` (new features).

3. **Edit** — AI applies fixes directly to the `_VBA/` text files using the Edit tool.

4. **Paste into VBE** — User opens Excel (`Alt+F11`), selects each modified module, replaces all code (`Ctrl+A` → `Delete` → `Ctrl+V`), saves (`Ctrl+S`).

5. **Verify** — Re-export and diff to confirm changes were applied correctly.

See `references/workflow.md` for the full step-by-step procedure.
See `references/vba-edit-recipes.md` for ready-to-use prompts.

---

## Key Scripts

### `scripts/export_vba.py`

Exports all VBA modules from a `.xlsm` file into a classified directory tree.

```
{basename}_VBA/
├── ExcelObjects/   ThisWorkbook, sheet modules  (.cls)
├── Forms/          UserForm modules              (.frm)
├── Modules/        standard modules              (.bas)
└── Classes/        class modules                 (.cls)
```

Module type is determined by file extension and the `Attribute VB_Base` GUID in the source:

| Condition | Folder |
|-----------|--------|
| `.bas` extension | `Modules/` |
| `.frm` extension | `Forms/` |
| `.cls` + VB_Base contains `00020819` or `00020820` | `ExcelObjects/` |
| `.cls` + VB_Base contains `B4C80393` | `Forms/` |
| other `.cls` | `Classes/` |

---

## Dependencies

```bash
pip install oletools    # required for export_vba.py
pip install openpyxl   # required if using xlsx-text-ops in the same session
```
