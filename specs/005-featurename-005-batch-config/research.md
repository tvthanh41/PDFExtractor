# Phase 0: Outline & Research

## Technical Context
- **Language/Version**: Python 3.x
- **Framework**: PySide6
- **Current Architecture**: MVC pattern with `AppController` handling tab and batch logic, and `TemplateRepository` handling persistence.

## Research Questions

### 1. Why does a template stay named "New Template" when loaded?
**Findings**: The `Template` object defaults to `name="New Template"`. When saved via `QFileDialog.getSaveFileName`, the `name` property is serialized into the JSON file. If the user saves it as `test.pdftpl`, the JSON still internally stores `"name": "New Template"`. When loaded back via `TemplateRepository.load`, it restores the "New Template" string. 

**Decision**: Modify `TemplateRepository.load` to enforce the template name to match the file's basename (stripping `.pdftpl`). Also, in `TemplateController.save_template`, update the `self.template.name` to match the chosen save filename, and emit a signal or call a method to update the workspace tab name so it reflects the new save name immediately.

### 2. How to implement the Batch Configuration Dialog?
**Findings**: Currently, `AppController.run_batch` sequentially prompts the user with three file dialogs and then immediately starts `batch_ctrl.start_batch(...)`. We need an intermediate confirmation step.

**Decision**: Create a new UI component `BatchConfigDialog` (inheriting from `QDialog`) that displays three read-only line edits (or labels) showing the selected paths. It will have "Start Batch" and "Cancel" buttons. The `AppController.run_batch` will instantiate this dialog after the file dialogs. If `dialog.exec()` is accepted, it proceeds to `start_batch`.
