from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QHeaderView, QMessageBox, QAbstractItemView, QLabel, QSpinBox)
from PySide6.QtCore import Qt
from src.ui.pdf_canvas import PdfCanvasWidget
from src.ui.rule_dialog import RuleDialog
from src.domain.models import BoundingBox
from src.i18n import t

class WorkspaceTabWidget(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_open = QPushButton(t("btn.open_pdf"))
        self.btn_open.setToolTip(t("tooltip.btn.open_pdf"))
        
        self.btn_add_rule = QPushButton(t("btn.add_rule"))
        self.btn_add_rule.setToolTip(t("tooltip.btn.add_rule"))
        
        self.btn_add_box = QPushButton(t("btn.add_box_rule"))
        self.btn_add_box.setToolTip(t("tooltip.btn.add_box_rule"))
        
        self.btn_add_table = QPushButton(t("btn.add_table_rule") if t("btn.add_table_rule") != "btn.add_table_rule" else "Add Table Rule")
        self.btn_add_table.setToolTip(t("tooltip.btn.add_table_rule") if t("tooltip.btn.add_table_rule") != "tooltip.btn.add_table_rule" else "Draw bounding box for a table rule")
        
        self.btn_save = QPushButton(t("btn.save_template"))
        self.btn_save.setToolTip(t("tooltip.btn.save_template"))
        
        self.btn_preview = QPushButton(t("btn.preview_extraction"))
        self.btn_preview.setToolTip(t("tooltip.btn.preview_extraction"))
        
        toolbar.addWidget(self.btn_open)
        toolbar.addWidget(self.btn_add_rule)
        toolbar.addWidget(self.btn_add_box)
        toolbar.addWidget(self.btn_add_table)
        toolbar.addWidget(self.btn_save)
        toolbar.addWidget(self.btn_preview)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Page Navigation Bar
        nav_bar = QHBoxLayout()
        self.btn_prev_page = QPushButton("◀")
        self.btn_prev_page.setFixedWidth(32)
        self.btn_prev_page.setToolTip(t("tooltip.btn.prev_page") if t("tooltip.btn.prev_page") != "tooltip.btn.prev_page" else "Previous Page")
        self.btn_prev_page.setEnabled(False)

        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(1)
        self.page_spin.setValue(1)
        self.page_spin.setFixedWidth(60)
        self.page_spin.setToolTip(t("tooltip.page_spin") if t("tooltip.page_spin") != "tooltip.page_spin" else "Current page (1-indexed)")
        self.page_spin.setEnabled(False)

        self.lbl_total_pages = QLabel("/ 0")
        self.lbl_total_pages.setFixedWidth(48)

        self.btn_next_page = QPushButton("▶")
        self.btn_next_page.setFixedWidth(32)
        self.btn_next_page.setToolTip(t("tooltip.btn.next_page") if t("tooltip.btn.next_page") != "tooltip.btn.next_page" else "Next Page")
        self.btn_next_page.setEnabled(False)

        nav_bar.addWidget(self.btn_prev_page)
        nav_bar.addWidget(self.page_spin)
        nav_bar.addWidget(self.lbl_total_pages)
        nav_bar.addWidget(self.btn_next_page)
        nav_bar.addStretch()
        layout.addLayout(nav_bar)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Canvas
        self.canvas = PdfCanvasWidget()
        splitter.addWidget(self.canvas)
        
        # Right side - Rules Table and Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.rules_table = QTableWidget(0, 5)
        self.rules_table.setHorizontalHeaderLabels([
            t("table.col.key"), 
            t("table.col.type"), 
            t("table.col.rule_type"),
            t("table.col.page") if t("table.col.page") != "table.col.page" else "Page",
            t("table.col.actions")
        ])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rules_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rules_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        right_layout.addWidget(self.rules_table)
        
        # Rule Actions
        rule_actions_layout = QHBoxLayout()
        self.btn_reselect = QPushButton(t("btn.reselect_region") if t("btn.reselect_region") != "btn.reselect_region" else "Reselect Region")
        self.btn_delete = QPushButton(t("btn.delete_rule") if t("btn.delete_rule") != "btn.delete_rule" else "Delete Rule")
        self.btn_reselect.setEnabled(False)
        self.btn_delete.setEnabled(False)
        rule_actions_layout.addWidget(self.btn_reselect)
        rule_actions_layout.addWidget(self.btn_delete)
        right_layout.addLayout(rule_actions_layout)
        
        self.preview_label = QLabel(t("label.preview_none"))
        self.preview_label.setWordWrap(True)
        right_layout.addWidget(self.preview_label)
        
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 300])
        layout.addWidget(splitter)
        
        # Connections
        self.btn_open.clicked.connect(self.controller.open_pdf)
        self.btn_add_rule.clicked.connect(self.controller.add_rule)
        self.btn_add_box.clicked.connect(self.toggle_box_mode)
        self.btn_add_table.clicked.connect(self.toggle_table_mode)
        self.btn_save.clicked.connect(self.controller.save_template)
        self.btn_preview.clicked.connect(self.controller.preview_extraction)
        
        self.canvas.box_selected.connect(self.on_box_selected)
        self.canvas.page_changed.connect(self.on_page_changed)
        self.rules_table.cellDoubleClicked.connect(self.on_rule_double_clicked)
        self.rules_table.itemSelectionChanged.connect(self.on_rule_selected)
        
        self.btn_reselect.clicked.connect(self.on_reselect_clicked)
        self.btn_delete.clicked.connect(self.on_delete_clicked)
        self.btn_prev_page.clicked.connect(self.canvas.prev_page)
        self.btn_next_page.clicked.connect(self.canvas.next_page)
        self.page_spin.valueChanged.connect(self._on_page_spin_changed)
        
    def on_rule_double_clicked(self, row, column):
        self.controller.edit_rule(row)

    def on_page_changed(self, current_page: int, total_pages: int):
        """Update navigation toolbar when canvas page changes."""
        # Block signals to avoid recursive loop with page_spin
        self.page_spin.blockSignals(True)
        self.page_spin.setMaximum(max(1, total_pages))
        self.page_spin.setValue(current_page + 1)  # display 1-indexed
        self.page_spin.blockSignals(False)
        self.lbl_total_pages.setText(f"/ {total_pages}")
        self.btn_prev_page.setEnabled(current_page > 0)
        self.btn_next_page.setEnabled(current_page < total_pages - 1)
        self.page_spin.setEnabled(total_pages > 1)

    def _on_page_spin_changed(self, value: int):
        """Navigate canvas when user edits page spinbox (1-indexed)."""
        self.canvas.set_page(value - 1)  # convert to 0-indexed
        
        
    def on_reselect_clicked(self):
        selected = self.rules_table.selectedItems()
        if selected:
            row = selected[0].row()
            self.controller.reselect_rule_region(row)
            
    def on_delete_clicked(self):
        selected = self.rules_table.selectedItems()
        if selected:
            row = selected[0].row()
            confirm = QMessageBox.question(
                self, 
                t("msg.confirm_delete") if t("msg.confirm_delete") != "msg.confirm_delete" else "Confirm Delete",
                t("msg.delete_rule_prompt") if t("msg.delete_rule_prompt") != "msg.delete_rule_prompt" else "Are you sure you want to delete this rule?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.controller.delete_rule(row)
        
    def on_preview_rule_clicked(self, button):
        for i in range(self.rules_table.rowCount()):
            if self.rules_table.cellWidget(i, 3) == button:
                self.controller.preview_single_rule(i)
                break
        
    def on_rule_selected(self):
        selected_items = self.rules_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.btn_delete.setEnabled(True)
            # We enable reselect based on rule type in controller, but for UI, we can just enable it and let controller check, or let controller enable it.
            # To keep UI simple, just enable it if a row is selected. Controller will ignore if not a bounding box rule.
            self.btn_reselect.setEnabled(True)
            self.controller.select_rule(row)
        else:
            self.btn_delete.setEnabled(False)
            self.btn_reselect.setEnabled(False)
            self.controller.select_rule(-1)
            
    def toggle_box_mode(self):
        self._is_table_mode = False
        self.canvas.toggle_selection_mode(True)

    def toggle_table_mode(self):
        self._is_table_mode = True
        self.canvas.toggle_selection_mode(True)
        
    def on_box_selected(self, x, y, w, h):
        self.canvas.toggle_selection_mode(False)
        box = BoundingBox(x_pct=x, y_pct=y, width_pct=w, height_pct=h)
        if hasattr(self.controller, 'reselecting_row') and self.controller.reselecting_row is not None:
            self.controller.finish_reselect_rule_region(box)
        elif getattr(self, '_is_table_mode', False):
            self.controller.add_table_rule(box)
        else:
            self.controller.add_box_rule(box)
        
    def add_rule_to_table(self, rule):
        row = self.rules_table.rowCount()
        self.rules_table.insertRow(row)
        self.rules_table.setItem(row, 0, QTableWidgetItem(rule.key_name))
        self.rules_table.setItem(row, 1, QTableWidgetItem(rule.data_type.value))
        self.rules_table.setItem(row, 2, QTableWidgetItem(rule.rule_type.value))
        page_idx = getattr(rule, 'page_index', 0)
        self.rules_table.setItem(row, 3, QTableWidgetItem(str(page_idx + 1)))  # 1-indexed display
        
        btn_preview = QPushButton(t("btn.preview"))
        btn_preview.setToolTip(t("tooltip.btn.preview_rule"))
        btn_preview.clicked.connect(lambda _, b=btn_preview: self.on_preview_rule_clicked(b))
        self.rules_table.setCellWidget(row, 4, btn_preview)
        
    def update_rule_in_table(self, row, rule):
        self.rules_table.setItem(row, 0, QTableWidgetItem(rule.key_name))
        self.rules_table.setItem(row, 1, QTableWidgetItem(rule.data_type.value))
        self.rules_table.setItem(row, 2, QTableWidgetItem(rule.rule_type.value))
        page_idx = getattr(rule, 'page_index', 0)
        self.rules_table.setItem(row, 3, QTableWidgetItem(str(page_idx + 1)))  # 1-indexed display

    def update_preview(self, text):
        if text == "None" or not text:
            self.preview_label.setText(t("label.preview_none"))
        else:
            self.preview_label.setText(t("label.preview").format(value=text))
        
    def show_error(self, message):
        QMessageBox.critical(self, t("msg.error"), message)
        
    def show_info(self, message):
        QMessageBox.information(self, t("msg.info"), message)

