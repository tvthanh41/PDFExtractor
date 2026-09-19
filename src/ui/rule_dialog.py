from pydantic import ValidationError
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QComboBox, QPushButton, QStackedWidget,
                               QWidget, QDoubleSpinBox, QSpinBox, QFormLayout,
                               QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from src.domain.enums import DataType, RuleType, SearchMode, Direction
from src.domain.models import AnchorExtractionRule, BoundingBoxExtractionRule, BoundingBox
from src.i18n import t
import uuid


class RuleDialog(QDialog):
    def __init__(self, parent=None, predefined_box=None, rule=None):
        super().__init__(parent)
        self.setWindowTitle(t("rule_dialog.title.edit") if rule else t("rule_dialog.title.create"))
        self.predefined_box = predefined_box if predefined_box else (rule.box if hasattr(rule, 'box') else None)
        self.rule_id = rule.rule_id if rule else str(uuid.uuid4())
        self.setup_ui()
        if rule:
            self._populate(rule)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # ── Common settings ──────────────────────────────────────────────
        form_layout = QFormLayout()

        self.key_name_input = QLineEdit()
        self.key_name_input.setPlaceholderText("e.g. total_amount")
        self.key_name_input.setToolTip(t("tooltip.rule_dialog.key_name"))
        form_layout.addRow(t("rule_dialog.label.key_name"), self.key_name_input)

        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems([e.value for e in DataType])
        self.data_type_combo.setToolTip(t("tooltip.rule_dialog.data_type"))
        form_layout.addRow(t("rule_dialog.label.data_type"), self.data_type_combo)

        self.rule_type_combo = QComboBox()
        self.rule_type_combo.addItems([e.value for e in RuleType])
        self.rule_type_combo.setToolTip(t("tooltip.rule_dialog.rule_type"))
        form_layout.addRow(t("rule_dialog.label.rule_type"), self.rule_type_combo)

        layout.addLayout(form_layout)

        # ── Stacked widget for rule-specific settings ─────────────────────
        self.stacked_widget = QStackedWidget()

        # ── Anchor page ───────────────────────────────────────────────────
        self.anchor_widget = QWidget()
        anchor_outer = QVBoxLayout(self.anchor_widget)
        anchor_outer.setContentsMargins(0, 0, 0, 0)

        anchor_basic = QFormLayout()
        self.anchor_text_input = QLineEdit()
        self.anchor_text_input.setToolTip(t("tooltip.rule_dialog.anchor_text"))
        
        self.search_mode_combo = QComboBox()
        self.search_mode_combo.addItems([e.value for e in SearchMode])
        self.search_mode_combo.setToolTip(t("tooltip.rule_dialog.search_mode"))
        
        self.direction_combo = QComboBox()
        self.direction_combo.addItems([e.value for e in Direction])
        self.direction_combo.setToolTip(t("tooltip.rule_dialog.direction"))
        
        anchor_basic.addRow(t("rule_dialog.label.anchor_text"), self.anchor_text_input)
        anchor_basic.addRow(t("rule_dialog.label.search_mode"), self.search_mode_combo)
        anchor_basic.addRow(t("rule_dialog.label.direction"), self.direction_combo)
        anchor_outer.addLayout(anchor_basic)

        # Anchor — Advanced toggle
        self.anchor_adv_btn = QPushButton(t("rule_dialog.label.advanced_collapsed"))
        self.anchor_adv_btn.setFlat(True)
        self.anchor_adv_btn.setCheckable(True)
        self.anchor_adv_btn.setStyleSheet("text-align: left; padding: 2px 0;")
        self.anchor_adv_btn.clicked.connect(self._toggle_anchor_advanced)
        anchor_outer.addWidget(self.anchor_adv_btn)

        # Anchor — Advanced group (hidden by default)
        self.anchor_adv_group = QGroupBox()
        self.anchor_adv_group.setFlat(True)
        adv_anchor_form = QFormLayout(self.anchor_adv_group)

        self.offset_distance_spin = QDoubleSpinBox()
        self.offset_distance_spin.setMinimum(0.0)
        self.offset_distance_spin.setMaximum(9999.0)
        self.offset_distance_spin.setSingleStep(10.0)
        self.offset_distance_spin.setValue(150.0)
        self.offset_distance_spin.setToolTip(t("tooltip.rule_dialog.offset_distance"))
        adv_anchor_form.addRow(t("rule_dialog.label.offset_distance"), self.offset_distance_spin)

        self.match_index_spin = QSpinBox()
        self.match_index_spin.setMinimum(0)
        self.match_index_spin.setMaximum(99)
        self.match_index_spin.setValue(0)
        self.match_index_spin.setToolTip(t("tooltip.rule_dialog.match_index"))
        adv_anchor_form.addRow(t("rule_dialog.label.match_index"), self.match_index_spin)

        self.anchor_adv_group.setVisible(False)
        anchor_outer.addWidget(self.anchor_adv_group)

        self.stacked_widget.addWidget(self.anchor_widget)

        # ── Bounding Box page ─────────────────────────────────────────────
        self.box_widget = QWidget()
        box_outer = QVBoxLayout(self.box_widget)
        box_outer.setContentsMargins(0, 0, 0, 0)

        self.box_label = QLabel(
            t("rule_dialog.label.box_defined") if self.predefined_box
            else t("rule_dialog.label.box_undefined")
        )
        box_outer.addWidget(self.box_label)

        # BoundingBox — Advanced toggle
        self.box_adv_btn = QPushButton(t("rule_dialog.label.advanced_collapsed"))
        self.box_adv_btn.setFlat(True)
        self.box_adv_btn.setCheckable(True)
        self.box_adv_btn.setStyleSheet("text-align: left; padding: 2px 0;")
        self.box_adv_btn.clicked.connect(self._toggle_box_advanced)
        box_outer.addWidget(self.box_adv_btn)

        # BoundingBox — Advanced group (hidden by default)
        self.box_adv_group = QGroupBox()
        self.box_adv_group.setFlat(True)
        adv_box_form = QFormLayout(self.box_adv_group)

        self.page_index_spin = QSpinBox()
        self.page_index_spin.setMinimum(0)
        self.page_index_spin.setMaximum(999)
        self.page_index_spin.setValue(0)
        self.page_index_spin.setToolTip(t("tooltip.rule_dialog.page_index"))
        adv_box_form.addRow(t("rule_dialog.label.page_index"), self.page_index_spin)

        self.box_adv_group.setVisible(False)
        box_outer.addWidget(self.box_adv_group)
        box_outer.addStretch()

        self.stacked_widget.addWidget(self.box_widget)

        layout.addWidget(self.stacked_widget)

        # ── Connections ───────────────────────────────────────────────────
        self.rule_type_combo.currentTextChanged.connect(self.on_rule_type_changed)

        # Set initial index
        if self.predefined_box:
            self.rule_type_combo.setCurrentText(RuleType.BOUNDING_BOX.value)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton(t("btn.save"))
        self.cancel_btn = QPushButton(t("btn.cancel"))
        self.save_btn.clicked.connect(self.on_save_clicked)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    # ── Toggle helpers ────────────────────────────────────────────────────

    def _toggle_anchor_advanced(self, checked: bool):
        self.anchor_adv_group.setVisible(checked)
        self.anchor_adv_btn.setText(
            t("rule_dialog.label.advanced_expanded") if checked else t("rule_dialog.label.advanced_collapsed")
        )
        self.adjustSize()

    def _toggle_box_advanced(self, checked: bool):
        self.box_adv_group.setVisible(checked)
        self.box_adv_btn.setText(
            t("rule_dialog.label.advanced_expanded") if checked else t("rule_dialog.label.advanced_collapsed")
        )
        self.adjustSize()

    # ── Rule type switch ──────────────────────────────────────────────────

    def on_rule_type_changed(self, rule_type):
        if rule_type == RuleType.ANCHOR_SEARCH.value:
            self.stacked_widget.setCurrentWidget(self.anchor_widget)
        else:
            self.stacked_widget.setCurrentWidget(self.box_widget)

    # ── Populate (edit mode) ──────────────────────────────────────────────

    def _populate(self, rule):
        self.key_name_input.setText(rule.key_name)
        self.data_type_combo.setCurrentText(rule.data_type.value)
        self.rule_type_combo.setCurrentText(rule.rule_type.value)

        if rule.rule_type == RuleType.ANCHOR_SEARCH:
            self.anchor_text_input.setText(rule.anchor_text)
            self.search_mode_combo.setCurrentText(rule.search_mode.value)
            self.direction_combo.setCurrentText(rule.direction.value)
            # Advanced anchor fields
            self.offset_distance_spin.setValue(rule.offset_distance)
            self.match_index_spin.setValue(rule.match_index)
            # Auto-expand if non-default values are stored
            has_non_defaults = (
                rule.offset_distance != 150.0 or rule.match_index != 0
            )
            if has_non_defaults:
                self.anchor_adv_btn.setChecked(True)
                self._toggle_anchor_advanced(True)
        else:
            # Advanced box field
            self.page_index_spin.setValue(rule.page_index)
            if rule.page_index != 0:
                self.box_adv_btn.setChecked(True)
                self._toggle_box_advanced(True)

    # ── Save ──────────────────────────────────────────────────────────────

    def on_save_clicked(self):
        try:
            self._rule = self._create_rule()
            self.accept()
        except ValidationError as e:
            error = e.errors()[0]
            field = error.get("loc", [""])[0]
            msg = error.get("msg", "Validation error")
            QMessageBox.warning(self, t("msg.validation_error"), f"Invalid '{field}': {msg}")
        except Exception as e:
            QMessageBox.warning(self, t("msg.error"), f"Unexpected error: {str(e)}")

    def _create_rule(self):
        rule_type = RuleType(self.rule_type_combo.currentText())
        data_type = DataType(self.data_type_combo.currentText())
        key_name = self.key_name_input.text()

        if rule_type == RuleType.ANCHOR_SEARCH:
            return AnchorExtractionRule(
                rule_id=self.rule_id,
                key_name=key_name,
                data_type=data_type,
                anchor_text=self.anchor_text_input.text(),
                search_mode=SearchMode(self.search_mode_combo.currentText()),
                direction=Direction(self.direction_combo.currentText()),
                offset_distance=self.offset_distance_spin.value(),
                match_index=self.match_index_spin.value(),
            )
        else:
            box = self.predefined_box if self.predefined_box else BoundingBox(
                x_pct=0, y_pct=0, width_pct=0, height_pct=0
            )
            return BoundingBoxExtractionRule(
                rule_id=self.rule_id,
                key_name=key_name,
                data_type=data_type,
                page_index=self.page_index_spin.value(),
                box=box,
            )

    def get_rule(self):
        return self._rule

