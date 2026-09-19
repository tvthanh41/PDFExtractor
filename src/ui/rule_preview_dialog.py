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
        self.text_edit.setPlainText(str(extracted_text) if extracted_text is not None else "")
        layout.addWidget(self.text_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_close = QPushButton(t("btn.close"))
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)

