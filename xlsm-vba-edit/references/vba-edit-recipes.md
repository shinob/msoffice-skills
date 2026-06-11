# VBA Edit Recipes

[日本語](vba-edit-recipes.ja.md)

Reusable prompts and patterns for AI-assisted VBA editing.

## Analysis Prompt

```text
Use msoffice-skills to analyze @{xlsm_file}.

Export the VBA modules, then write a report named {xlsm_file}_analysis.md with:
1. Workbook overview: sheets, modules, and main features.
2. Issues grouped by priority:
   - High: bugs and crash risks.
   - Medium: incomplete or broken features.
   - Low: maintainability and code quality.
3. For each issue: location, problem, proposed fix, and code example when useful.
4. Recommended fix order and validation checklist.
```

## Feature Planning Prompt

```text
Use msoffice-skills to inspect @{xlsm_file} and summarize the current workbook and VBA features.

Then ask focused questions about the desired feature:
1. Goal and user scenario.
2. Expected operation: menu, button, event, or automatic behavior.
3. Priority and deadline.

Write the result to {xlsm_file}_features.md with feasibility, implementation approach, impact, effort estimate, recommended order, and validation checklist.
```

## Apply Fixes Prompt

```text
Review @{xlsm_file}_analysis.md.
Apply the selected fixes to the relevant files under @{xlsm_file}_VBA/.

When finished, report:
1. Files changed.
2. Summary of each change.
3. Exact VBE paste-back instructions: folder, file, and target module.
```

## Verification Prompt

```text
The updated code has been pasted into VBE and saved.
Run export_vba.py again and compare the exported modules with the edited files.
Report whether the workbook contains the intended changes only.
```

## Recommended Order

1. Export VBA.
2. Create an analysis report.
3. Plan features only after high-priority defects are understood.
4. Apply one high-risk fix at a time.
5. Paste back through VBE.
6. Re-export and diff.
