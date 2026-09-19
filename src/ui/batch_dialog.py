from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QProgressBar, QTextEdit)
from PySide6.QtCore import Qt
from src.i18n import t

class BatchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("batch_progress.title"))
        self.resize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.lbl_completed = QLabel(t("batch_progress.completed").format(completed=0, total=0))
        self.lbl_failed = QLabel(t("batch_progress.failed").format(failed=0))
        stats_layout.addWidget(self.lbl_completed)
        stats_layout.addStretch()
        stats_layout.addWidget(self.lbl_failed)
        layout.addLayout(stats_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Actions
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton(t("btn.cancel"))
        self.btn_close = QPushButton(t("btn.close"))
        self.btn_close.setEnabled(False)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)
        
        # Connections
        self.btn_close.clicked.connect(self.accept)
        
    def update_progress(self, completed: int, total: int, failed: int):
        self.lbl_completed.setText(t("batch_progress.completed").format(completed=completed, total=total))
        self.lbl_failed.setText(t("batch_progress.failed").format(failed=failed))
        if total > 0:
            pct = int((completed / total) * 100)
            self.progress_bar.setValue(pct)
            
    def append_log(self, msg: str):
        self.log_text.append(msg)
        
    def processing_finished(self):
        self.btn_cancel.setEnabled(False)
        self.btn_close.setEnabled(True)
        self.append_log(t("batch_progress.finished"))

