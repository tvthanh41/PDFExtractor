from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QTextEdit,
    QPushButton, QHeaderView, QSizePolicy,
)
from PySide6.QtCore import Qt
from src.i18n import t


class RulePreviewDialog(QDialog):
    """
    Preview dialog for a single extraction rule result.

    - list[list]: rendered as an Excel-like QTableWidget grid, with the first
      row treated as a header if the table has more than one row.
    - dict:       rendered as a two-column key/value QTableWidget.
    - anything else: rendered as plain text in a read-only QTextEdit.
    """

    def __init__(self, key_name, extracted_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("rule_preview_dialog.title").format(key=key_name))
        self.resize(700, 480)
        self.setSizeGripEnabled(True)

        layout = QVBoxLayout(self)

        # ── Content area ────────────────────────────────────────────────────
        if isinstance(extracted_text, list) and extracted_text and isinstance(extracted_text[0], list):
            widget = self._build_grid_table(extracted_text)
        elif isinstance(extracted_text, dict):
            widget = self._build_kv_table(extracted_text)
        else:
            widget = self._build_text_view(extracted_text)

        layout.addWidget(widget)

        # ── Buttons ─────────────────────────────────────────────────────────
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_close = QPushButton(t("btn.close"))
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

    # ── Builders ──────────────────────────────────────────────────────────

    def _build_grid_table(self, data: list) -> QTableWidget:
        """Render a list[list] as an Excel-style grid with a frozen header row."""
        num_rows = len(data)
        num_cols = max(len(row) for row in data) if data else 0

        has_header = num_rows > 1

        if has_header:
            header_labels = [str(cell) for cell in data[0]]
            body = data[1:]
        else:
            header_labels = [str(i + 1) for i in range(num_cols)]
            body = data

        table = QTableWidget(len(body), num_cols)
        table.setHorizontalHeaderLabels(header_labels)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setDefaultSectionSize(24)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for r_idx, row in enumerate(body):
            for c_idx in range(num_cols):
                cell_val = row[c_idx] if c_idx < len(row) else ""
                item = QTableWidgetItem(str(cell_val) if cell_val is not None else "")
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                table.setItem(r_idx, c_idx, item)

        table.resizeRowsToContents()
        return table

    def _build_kv_table(self, data: dict) -> QTableWidget:
        """Render a dict as a two-column Key / Value table."""
        table = QTableWidget(len(data), 2)
        table.setHorizontalHeaderLabels(["Key", "Value"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for r_idx, (key, val) in enumerate(data.items()):
            key_item = QTableWidgetItem(str(key))
            key_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            val_item = QTableWidgetItem(str(val) if val is not None else "")
            val_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            table.setItem(r_idx, 0, key_item)
            table.setItem(r_idx, 1, val_item)

        table.resizeRowsToContents()
        return table

    def _build_text_view(self, data) -> QTextEdit:
        """Fallback: render scalar or None values as plain read-only text."""
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(str(data) if data is not None else "")
        return text_edit
