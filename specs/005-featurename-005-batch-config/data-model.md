# Data Model & Contracts

No changes to the persistent data model (`Template`, `ExtractionRule`) are required for this feature, other than enforcing that `Template.name` tracks the filename appropriately in memory when loading/saving.

## UI Contracts

### `BatchConfigDialog`
A new QDialog component to present the configuration before batch execution.
- **Inputs**: 
  - `template_path`: str
  - `input_dir`: str
  - `output_csv`: str
- **Outputs**:
  - `Accepted` or `Rejected` DialogCode
- **Elements**:
  - Labels indicating the paths.
  - "Start Batch" button (accept).
  - "Cancel" button (reject).

### `WorkspaceTabWidget` Update
- To support renaming the tab upon Save, the `WorkspaceTabWidget` or `AppController` needs a way to update the tab text.
- Currently, `AppController` sets the tab title at creation: `self.main_window.add_workspace_tab(view, template.name)`.
- We will add a method in `AppController` or pass a callback to `TemplateController` to allow renaming the tab title in the QTabWidget when `save_template` is successfully executed.
