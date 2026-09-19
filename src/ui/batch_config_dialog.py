from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QFileDialog
)
from PySide6.QtGui import QFont
from src.i18n import t


class BatchConfigDialog(QDialog):
    """
    A full configuration dialog for starting a batch extraction job.
    Users can browse for the template, input folder, and output CSV directly
    in this dialog — no separate file picker prompts needed.
    The 'Start Batch' button is only enabled once all three paths are filled.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("batch_dialog.title"))
        self.setMinimumWidth(620)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # --- Title ---
        title = QLabel(t("batch_dialog.heading"))
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        subtitle = QLabel(t("batch_dialog.subtitle"))
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(sep1)

        # --- Path fields ---
        self._template_edit = self._make_edit()
        self._template_edit.setToolTip(t("tooltip.batch_dialog.template"))
        
        self._input_edit = self._make_edit()
        self._input_edit.setToolTip(t("tooltip.batch_dialog.input_dir"))
        
        self._output_edit = self._make_edit()
        self._output_edit.setToolTip(t("tooltip.batch_dialog.output_csv"))

        layout.addLayout(self._labeled_browse_row(
            t("batch_dialog.label.template"), self._template_edit, t("btn.browse"), self._browse_template
        ))
        layout.addLayout(self._labeled_browse_row(
            t("batch_dialog.label.input_dir"), self._input_edit, t("btn.browse"), self._browse_input_dir
        ))
        layout.addLayout(self._labeled_browse_row(
            t("batch_dialog.label.output_csv"), self._output_edit, t("btn.save_as"), self._browse_output_csv
        ))

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(sep2)

        # --- Buttons ---
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()

        cancel_btn = QPushButton(t("btn.cancel"))
        cancel_btn.setObjectName("cancelBatchBtn")
        cancel_btn.setMinimumWidth(90)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        self._start_btn = QPushButton(t("btn.start_batch"))
        self._start_btn.setObjectName("startBatchBtn")
        self._start_btn.setMinimumWidth(110)
        self._start_btn.setDefault(True)
        self._start_btn.setEnabled(False)
        self._start_btn.clicked.connect(self.accept)
        btn_row.addWidget(self._start_btn)

        layout.addLayout(btn_row)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_edit(self) -> QLineEdit:
        edit = QLineEdit()
        edit.setPlaceholderText(t("batch_dialog.placeholder.not_selected"))
        edit.textChanged.connect(self._validate)
        return edit

    def _labeled_browse_row(self, label_text: str, line_edit: QLineEdit,
                             btn_text: str, browse_fn) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(4)

        label = QLabel(label_text)
        bold = QFont()
        bold.setBold(True)
        label.setFont(bold)
        col.addWidget(label)

        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(line_edit)

        btn = QPushButton(btn_text)
        btn.setFixedWidth(90)
        btn.clicked.connect(browse_fn)
        row.addWidget(btn)

        col.addLayout(row)
        return col

    # ------------------------------------------------------------------
    # Browse callbacks
    # ------------------------------------------------------------------

    def _browse_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Template", "", "Template Files (*.pdftpl)"
        )
        if path:
            self._template_edit.setText(path)

    def _browse_input_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Input PDF Folder")
        if path:
            self._input_edit.setText(path)

    def _browse_output_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Results CSV", "results.csv", "CSV Files (*.csv)"
        )
        if path:
            self._output_edit.setText(path)

    def _validate(self):
        """Enable Start Batch only when all three paths are provided."""
        all_filled = bool(
            self._template_edit.text().strip()
            and self._input_edit.text().strip()
            and self._output_edit.text().strip()
        )
        self._start_btn.setEnabled(all_filled)

    # ------------------------------------------------------------------
    # Properties for the caller to read selections
    # ------------------------------------------------------------------

    @property
    def template_path(self) -> str:
        return self._template_edit.text().strip()

    @property
    def input_dir(self) -> str:
        return self._input_edit.text().strip()

    @property
    def output_csv(self) -> str:
        return self._output_edit.text().strip()

