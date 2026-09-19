import csv
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QPushButton, QHeaderView, QFileDialog, QMessageBox)
from src.i18n import t

class PreviewDialog(QDialog):
    def __init__(self, results_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("preview_dialog.title"))
        self.resize(800, 400)
        self.results_dict = results_dict
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget(1, len(self.results_dict))
        self.table.setHorizontalHeaderLabels(list(self.results_dict.keys()))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        # Populate the single row with values
        for col, value in enumerate(self.results_dict.values()):
            item = QTableWidgetItem(str(value) if value is not None else "")
            self.table.setItem(0, col, item)

        # Allow rows to resize based on content (e.g. if a value is large)
        self.table.resizeRowsToContents()

        layout.addWidget(self.table)

        # Button layout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_export = QPushButton(t("btn.export"))
        self.btn_export.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.btn_export)

        self.btn_close = QPushButton(t("btn.close"))
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

    def export_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "preview_extraction.csv", "CSV Files (*.csv)"
        )
        if file_name:
            try:
                with open(file_name, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write headers
                    writer.writerow(self.results_dict.keys())
                    # Write values
                    writer.writerow(self.results_dict.values())
                QMessageBox.information(self, t("msg.info"), f"Successfully exported to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, t("msg.error"), f"Failed to export CSV:\n{str(e)}")

