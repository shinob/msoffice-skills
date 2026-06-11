# XLSM VBA Edit Workflow

[日本語](workflow.ja.md)

This workflow helps an AI assistant analyze and edit VBA code from an `.xlsm` workbook. The assistant edits exported text files; the user applies changes manually through Excel's Visual Basic Editor (VBE).

## Requirements

- Python 3.9 or later
- Microsoft Excel for VBE paste-back
- `oletools`

```bash
pip install oletools
```

Install `openpyxl` only when using `xlsx-text-ops` in the same task.

## Workflow

1. **Create a backup**
   ```bash
   cp target.xlsm target_backup_YYYYMMDD.xlsm
   ```

2. **Export VBA**
   ```bash
   python3 xlsm-vba-edit/scripts/export_vba.py target.xlsm
   ```

   Output:
   ```text
   target_VBA/
   ├── ExcelObjects/
   ├── Forms/
   ├── Modules/
   └── Classes/
   ```

3. **Analyze or plan**
   Use `vba-edit-recipes.md` to produce either:
   - `{basename}_analysis.md` for bug and quality review
   - `{basename}_features.md` for feature planning

4. **Edit exported code**
   The assistant edits files under `{basename}_VBA/` directly.

5. **Paste into VBE**
   The user opens Excel, presses `Alt+F11`, selects each changed module, replaces its code, and saves the workbook.

6. **Verify**
   Re-export VBA and compare the exported modules with the edited files.

## Troubleshooting

| Issue | Action |
|-------|--------|
| VBE shows a syntax error | Paste the exact error back to the assistant and revise the module |
| Text encoding looks wrong | Re-export with `export_vba.py` and compare encodings |
| Diff contains unexpected changes | Review whether VBE normalized attributes, spacing, or line endings |
| Behavior changed unexpectedly | Return to analysis, identify the affected procedure, and narrow the fix |

## Rollback

Restore the backup workbook:

```bash
cp target_backup_YYYYMMDD.xlsm target.xlsm
```
