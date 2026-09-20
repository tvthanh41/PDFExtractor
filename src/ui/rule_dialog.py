from pydantic import ValidationError
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QComboBox, QPushButton, QStackedWidget,
                               QWidget, QDoubleSpinBox, QSpinBox, QFormLayout,
                               QMessageBox, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt
from src.domain.enums import DataType, RuleType, SearchMode, Direction, TableStrategy, TableBoundaryType, TableEngine
from src.domain.models import (AnchorExtractionRule, BoundingBoxExtractionRule, BoundingBox,
                               TableExtractionRule, TableConfig, PatternBoundaryConfig)
from src.i18n import t
import uuid


class RuleDialog(QDialog):
    def __init__(self, parent=None, predefined_box=None, rule=None, default_page_index: int = 0):
        super().__init__(parent)
        self.setWindowTitle(t("rule_dialog.title.edit") if rule else t("rule_dialog.title.create"))
        self.predefined_box = predefined_box if predefined_box else (rule.box if hasattr(rule, 'box') else None)
        self.rule_id = rule.rule_id if rule else str(uuid.uuid4())
        self._default_page_index = default_page_index
        self.setup_ui()
        if rule:
            self._populate(rule)
        elif default_page_index > 0:
            # Apply default page index for new rules when viewing non-first page
            self.page_index_spin.setValue(default_page_index)
            self.table_page_index_spin.setValue(default_page_index)
            self.anchor_page_index_spin.setValue(default_page_index)

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

        # Anchor page index (which page to search)
        self.anchor_page_index_spin = QSpinBox()
        self.anchor_page_index_spin.setMinimum(0)
        self.anchor_page_index_spin.setMaximum(9999)
        self.anchor_page_index_spin.setValue(0)
        self.anchor_page_index_spin.setToolTip(t("tooltip.rule_dialog.page_index"))
        adv_anchor_form.addRow(t("rule_dialog.label.page_index"), self.anchor_page_index_spin)

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

        # ── Table page ───────────────────────────────────────────────────
        self.table_widget = QWidget()
        table_outer = QVBoxLayout(self.table_widget)
        table_outer.setContentsMargins(0, 0, 0, 0)

        # Boundary mode selector (always visible)
        boundary_form = QFormLayout()
        self.table_boundary_combo = QComboBox()
        self.table_boundary_combo.addItem("Bounding Box", TableBoundaryType.BOUNDING_BOX)
        self.table_boundary_combo.addItem("Pattern Match", TableBoundaryType.PATTERN_MATCH)
        self.table_boundary_combo.setToolTip(t("tooltip.rule_dialog.boundary_mode"))
        boundary_form.addRow(t("rule_dialog.label.boundary_mode"), self.table_boundary_combo)
        table_outer.addLayout(boundary_form)

        # Box label (shown when bounding box mode)
        self.table_label = QLabel(
            t("rule_dialog.label.table_box_defined") if self.predefined_box
            else t("rule_dialog.label.table_box_undefined")
        )
        table_outer.addWidget(self.table_label)

        # Pattern boundary group (shown when pattern match mode)
        self.pattern_boundary_group = QGroupBox("Pattern Boundary")
        pb_form = QFormLayout(self.pattern_boundary_group)

        self.start_pattern_input = QLineEdit()
        self.start_pattern_input.setPlaceholderText("e.g. Item Description")
        self.start_pattern_input.setToolTip(t("tooltip.rule_dialog.start_pattern"))
        pb_form.addRow(t("rule_dialog.label.start_pattern"), self.start_pattern_input)

        self.end_pattern_input = QLineEdit()
        self.end_pattern_input.setPlaceholderText("e.g. Subtotal")
        self.end_pattern_input.setToolTip(t("tooltip.rule_dialog.end_pattern"))
        pb_form.addRow(t("rule_dialog.label.end_pattern"), self.end_pattern_input)

        self.include_start_check = QCheckBox()
        self.include_start_check.setChecked(True)
        self.include_start_check.setToolTip(t("tooltip.rule_dialog.include_start"))
        pb_form.addRow(t("rule_dialog.label.include_start"), self.include_start_check)

        self.include_end_check = QCheckBox()
        self.include_end_check.setChecked(False)
        self.include_end_check.setToolTip(t("tooltip.rule_dialog.include_end"))
        pb_form.addRow(t("rule_dialog.label.include_end"), self.include_end_check)

        self.is_regex_check = QCheckBox()
        self.is_regex_check.setChecked(False)
        self.is_regex_check.setToolTip(t("tooltip.rule_dialog.use_regex"))
        pb_form.addRow(t("rule_dialog.label.use_regex"), self.is_regex_check)

        self.skip_k_spin = QSpinBox()
        self.skip_k_spin.setMinimum(0)
        self.skip_k_spin.setMaximum(999)
        self.skip_k_spin.setValue(0)
        self.skip_k_spin.setToolTip(t("tooltip.rule_dialog.skip_k"))
        pb_form.addRow(t("rule_dialog.label.skip_k"), self.skip_k_spin)

        self.pattern_boundary_group.setVisible(False)
        table_outer.addWidget(self.pattern_boundary_group)

        # Connect boundary mode change
        self.table_boundary_combo.currentIndexChanged.connect(self._on_table_boundary_mode_changed)

        # Table — Advanced toggle
        self.table_adv_btn = QPushButton(t("rule_dialog.label.advanced_collapsed"))
        self.table_adv_btn.setFlat(True)
        self.table_adv_btn.setCheckable(True)
        self.table_adv_btn.setStyleSheet("text-align: left; padding: 2px 0;")
        self.table_adv_btn.clicked.connect(self._toggle_table_advanced)
        table_outer.addWidget(self.table_adv_btn)

        # Table — Advanced group (hidden by default)
        self.table_adv_group = QGroupBox()
        self.table_adv_group.setFlat(True)
        adv_table_form = QFormLayout(self.table_adv_group)

        self.table_page_index_spin = QSpinBox()
        self.table_page_index_spin.setMinimum(0)
        self.table_page_index_spin.setMaximum(999)
        self.table_page_index_spin.setValue(0)
        self.table_page_index_spin.setToolTip(t("tooltip.rule_dialog.page_index"))
        adv_table_form.addRow(t("rule_dialog.label.page_index"), self.table_page_index_spin)

        # Engine selector
        self.table_engine_combo = QComboBox()
        self.table_engine_combo.addItem("PyMuPDF (Native)", TableEngine.PYMUPDF)
        self.table_engine_combo.addItem("PyMuPDF4LLM (Layout Markdown)", TableEngine.PYMUPDF4LLM)
        self.table_engine_combo.setToolTip(t("tooltip.rule_dialog.extraction_engine"))
        adv_table_form.addRow(t("rule_dialog.label.extraction_engine"), self.table_engine_combo)

        self.table_has_borders_check = QCheckBox()
        self.table_has_borders_check.setChecked(True)
        self.table_has_borders_check.setToolTip(t("tooltip.rule_dialog.has_borders"))
        adv_table_form.addRow(t("rule_dialog.label.has_borders"), self.table_has_borders_check)

        self.table_as_kv_check = QCheckBox()
        self.table_as_kv_check.setChecked(False)
        self.table_as_kv_check.setToolTip(t("tooltip.rule_dialog.extract_as_key_value"))
        adv_table_form.addRow(t("rule_dialog.label.extract_as_key_value"), self.table_as_kv_check)

        self.table_vert_strat_combo = QComboBox()
        self.table_vert_strat_combo.addItems([e.value for e in TableStrategy])
        self.table_vert_strat_combo.setCurrentText(TableStrategy.LINES.value)
        self.table_vert_strat_combo.setToolTip(t("tooltip.rule_dialog.vertical_strategy"))
        adv_table_form.addRow(t("rule_dialog.label.vertical_strategy"), self.table_vert_strat_combo)

        self.table_horiz_strat_combo = QComboBox()
        self.table_horiz_strat_combo.addItems([e.value for e in TableStrategy])
        self.table_horiz_strat_combo.setCurrentText(TableStrategy.LINES.value)
        self.table_horiz_strat_combo.setToolTip(t("tooltip.rule_dialog.horizontal_strategy"))
        adv_table_form.addRow(t("rule_dialog.label.horizontal_strategy"), self.table_horiz_strat_combo)

        self.table_header_rows_spin = QSpinBox()
        self.table_header_rows_spin.setMinimum(0)
        self.table_header_rows_spin.setMaximum(99)
        self.table_header_rows_spin.setValue(1)
        self.table_header_rows_spin.setToolTip(t("tooltip.rule_dialog.header_rows_count"))
        adv_table_form.addRow(t("rule_dialog.label.header_rows_count"), self.table_header_rows_spin)

        self.table_snap_tol_spin = QDoubleSpinBox()
        self.table_snap_tol_spin.setMinimum(0.0)
        self.table_snap_tol_spin.setMaximum(100.0)
        self.table_snap_tol_spin.setValue(3.0)
        self.table_snap_tol_spin.setSingleStep(0.5)
        self.table_snap_tol_spin.setToolTip(t("tooltip.rule_dialog.snap_tolerance"))
        adv_table_form.addRow(t("rule_dialog.label.snap_tolerance"), self.table_snap_tol_spin)

        self.table_adv_group.setVisible(False)
        table_outer.addWidget(self.table_adv_group)
        table_outer.addStretch()

        self.stacked_widget.addWidget(self.table_widget)

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

    def _toggle_table_advanced(self, checked: bool):
        self.table_adv_group.setVisible(checked)
        self.table_adv_btn.setText(
            t("rule_dialog.label.advanced_expanded") if checked else t("rule_dialog.label.advanced_collapsed")
        )
        self.adjustSize()

    def _on_table_boundary_mode_changed(self, index: int):
        """Show/hide pattern boundary group and box label based on selected boundary mode."""
        mode = self.table_boundary_combo.currentData()
        is_pattern = (mode == TableBoundaryType.PATTERN_MATCH)
        self.pattern_boundary_group.setVisible(is_pattern)
        self.table_label.setVisible(not is_pattern)
        # Update the page-index spin tooltip to reflect its role in each mode
        if is_pattern:
            self.table_page_index_spin.setToolTip(t("tooltip.rule_dialog.pattern_start_page"))
        else:
            self.table_page_index_spin.setToolTip(t("tooltip.rule_dialog.page_index"))
        self.adjustSize()

    # ── Rule type switch ──────────────────────────────────────────────────

    def on_rule_type_changed(self, rule_type):
        if rule_type == RuleType.ANCHOR_SEARCH.value:
            self.stacked_widget.setCurrentWidget(self.anchor_widget)
        elif rule_type == RuleType.TABLE.value:
            self.stacked_widget.setCurrentWidget(self.table_widget)
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
            self.anchor_page_index_spin.setValue(getattr(rule, 'page_index', 0))
            # Auto-expand if non-default values are stored
            has_non_defaults = (
                rule.offset_distance != 150.0 or rule.match_index != 0
                or getattr(rule, 'page_index', 0) != 0
            )
            if has_non_defaults:
                self.anchor_adv_btn.setChecked(True)
                self._toggle_anchor_advanced(True)
        elif rule.rule_type == RuleType.TABLE:
            self.table_page_index_spin.setValue(rule.page_index)
            # Restore boundary mode
            boundary_type = getattr(rule, 'boundary_type', TableBoundaryType.BOUNDING_BOX)
            idx = self.table_boundary_combo.findData(boundary_type)
            if idx >= 0:
                self.table_boundary_combo.setCurrentIndex(idx)
            # Restore pattern boundary fields
            pb = getattr(rule, 'pattern_boundary', None)
            if pb:
                self.start_pattern_input.setText(pb.start_pattern)
                self.end_pattern_input.setText(pb.end_pattern)
                self.include_start_check.setChecked(pb.include_start)
                self.include_end_check.setChecked(pb.include_end)
                self.is_regex_check.setChecked(pb.is_regex)
                self.skip_k_spin.setValue(pb.skip_k)
            # Restore engine
            engine = getattr(rule.config, 'engine', TableEngine.PYMUPDF)
            engine_idx = self.table_engine_combo.findData(engine)
            if engine_idx >= 0:
                self.table_engine_combo.setCurrentIndex(engine_idx)
            self.table_has_borders_check.setChecked(rule.config.has_borders)
            self.table_as_kv_check.setChecked(getattr(rule.config, 'extract_as_key_value', False))
            self.table_vert_strat_combo.setCurrentText(rule.config.vertical_strategy.value)
            self.table_horiz_strat_combo.setCurrentText(rule.config.horizontal_strategy.value)
            self.table_header_rows_spin.setValue(rule.config.header_rows_count)
            self.table_snap_tol_spin.setValue(rule.config.snap_tolerance)
            has_non_defaults = (
                rule.page_index != 0 or
                not rule.config.has_borders or
                getattr(rule.config, 'extract_as_key_value', False) or
                rule.config.vertical_strategy != TableStrategy.LINES or
                rule.config.horizontal_strategy != TableStrategy.LINES or
                rule.config.header_rows_count != 1 or
                rule.config.snap_tolerance != 3.0 or
                engine != TableEngine.PYMUPDF
            )
            if has_non_defaults:
                self.table_adv_btn.setChecked(True)
                self._toggle_table_advanced(True)
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
                page_index=self.anchor_page_index_spin.value(),
            )
        elif rule_type == RuleType.TABLE:
            boundary_type = self.table_boundary_combo.currentData()
            engine = self.table_engine_combo.currentData()
            config = TableConfig(
                has_borders=self.table_has_borders_check.isChecked(),
                extract_as_key_value=self.table_as_kv_check.isChecked(),
                vertical_strategy=TableStrategy(self.table_vert_strat_combo.currentText()),
                horizontal_strategy=TableStrategy(self.table_horiz_strat_combo.currentText()),
                header_rows_count=self.table_header_rows_spin.value(),
                snap_tolerance=self.table_snap_tol_spin.value(),
                engine=engine,
            )
            if boundary_type == TableBoundaryType.PATTERN_MATCH:
                pattern_boundary = PatternBoundaryConfig(
                    start_pattern=self.start_pattern_input.text(),
                    end_pattern=self.end_pattern_input.text(),
                    include_start=self.include_start_check.isChecked(),
                    include_end=self.include_end_check.isChecked(),
                    is_regex=self.is_regex_check.isChecked(),
                    skip_k=self.skip_k_spin.value(),
                )
                return TableExtractionRule(
                    rule_id=self.rule_id,
                    key_name=key_name,
                    data_type=data_type,
                    page_index=self.table_page_index_spin.value(),
                    boundary_type=TableBoundaryType.PATTERN_MATCH,
                    pattern_boundary=pattern_boundary,
                    config=config,
                )
            else:
                box = self.predefined_box if self.predefined_box else BoundingBox(
                    x_pct=0, y_pct=0, width_pct=0, height_pct=0
                )
                return TableExtractionRule(
                    rule_id=self.rule_id,
                    key_name=key_name,
                    data_type=data_type,
                    page_index=self.table_page_index_spin.value(),
                    boundary_type=TableBoundaryType.BOUNDING_BOX,
                    box=box,
                    config=config,
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

