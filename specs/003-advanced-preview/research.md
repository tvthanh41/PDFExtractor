# Research: Advanced Preview

## Displaying Spreadsheet Data in PySide6
- **Decision**: Use `QTableWidget` instead of `QTableView` with a custom model.
- **Rationale**: The extraction preview data is extremely simple (a flat dictionary of keys and values representing a single row). A full `QAbstractTableModel` is overkill for 1 row of data. `QTableWidget` allows us to easily populate headers and resize columns natively via `QHeaderView.Interactive`.
- **Alternatives considered**: `QTableView` with `QStandardItemModel` (rejected due to unnecessary boilerplate).

## Exporting to CSV
- **Decision**: Use Python's built-in `csv` module.
- **Rationale**: The `csv.writer` perfectly handles escaping newline characters and commas within large blocks of extracted text, which is critical since our extracted values can be massive strings.
- **Alternatives considered**: Manual string formatting (rejected due to edge cases with quotes and commas).

## Per-Rule Preview Buttons
- **Decision**: Embed `QPushButton` inside the `QTableWidget` using `setCellWidget`.
- **Rationale**: This provides immediate discoverability for the user. We will wire the button click to resolve its row dynamically rather than relying on stale closures.
- **Alternatives considered**: A context menu on right-click (rejected because it is less discoverable), or a dedicated button in the `RuleDialog` (rejected because it forces the user to open the edit dialog just to preview).
