from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from src.i18n import t

class RulePreviewDialog(QDialog):
    def __init__(self, key_name, extracted_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("rule_preview_dialog.title").format(key=key_name))
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        
        if isinstance(extracted_text, dict):
            max_k_len = max([len(str(k)) for k in extracted_text.keys()] or [0])
            lines = [f"{str(k).ljust(max_k_len)} : {str(v)}" for k, v in extracted_text.items()]
            display_text = "\n".join(lines)
        elif isinstance(extracted_text, list) and extracted_text and isinstance(extracted_text[0], list):
            col_widths = {}
            for row in extracted_text:
                for idx, cell in enumerate(row):
                    col_widths[idx] = max(col_widths.get(idx, 0), len(str(cell)))
            lines = []
            for row_idx, row in enumerate(extracted_text):
                formatted_cells = [str(cell).ljust(col_widths.get(idx, 0)) for idx, cell in enumerate(row)]
                lines.append(" | ".join(formatted_cells))
                if row_idx == 0 and len(extracted_text) > 1:
                    lines.append("-+-".join("-" * col_widths.get(idx, 0) for idx in range(len(row))))
            display_text = "\n".join(lines)
        else:
            display_text = str(extracted_text) if extracted_text is not None else ""
            
        self.text_edit.setPlainText(display_text)
        layout.addWidget(self.text_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_close = QPushButton(t("btn.close"))
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)

