import pytest
from PySide6.QtWidgets import QApplication
from src.domain.enums import DataType, RuleType, TableStrategy
from src.domain.models import BoundingBox, TableConfig, TableExtractionRule
from src.ui.rule_dialog import RuleDialog
from src.ui.pdf_canvas import PdfCanvasWidget

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_rule_dialog_table_creation(qapp):
    box = BoundingBox(x_pct=0.1, y_pct=0.2, width_pct=0.7, height_pct=0.4)
    dialog = RuleDialog(predefined_box=box)
    dialog.rule_type_combo.setCurrentText(RuleType.TABLE.value)
    dialog.key_name_input.setText("invoice_items")
    dialog.data_type_combo.setCurrentText(DataType.STRING.value)
    
    rule = dialog._create_rule()
    assert isinstance(rule, TableExtractionRule)
    assert rule.rule_type == RuleType.TABLE
    assert rule.key_name == "invoice_items"
    assert rule.box.x_pct == 0.1
    assert rule.box.width_pct == 0.7

def test_rule_dialog_table_populate(qapp):
    box = BoundingBox(x_pct=0.05, y_pct=0.1, width_pct=0.85, height_pct=0.5)
    orig_rule = TableExtractionRule(
        key_name="my_table",
        data_type=DataType.STRING,
        box=box,
        page_index=2,
        config=TableConfig(has_borders=False, vertical_strategy=TableStrategy.TEXT, header_rows_count=2)
    )
    dialog = RuleDialog(rule=orig_rule)
    assert dialog.rule_type_combo.currentText() == RuleType.TABLE.value
    assert dialog.key_name_input.text() == "my_table"
    
    updated_rule = dialog._create_rule()
    assert isinstance(updated_rule, TableExtractionRule)
    assert updated_rule.key_name == "my_table"
    assert updated_rule.page_index == 2

def test_canvas_table_highlight(qapp):
    from PySide6.QtGui import QPixmap
    canvas = PdfCanvasWidget()
    pix = QPixmap(100, 100)
    canvas.pixmap_item = canvas.scene.addPixmap(pix)
    box = BoundingBox(x_pct=0.1, y_pct=0.1, width_pct=0.5, height_pct=0.5)
    # Highlight box as a table rule
    canvas.highlight_box(box, is_table=True)
    assert canvas.highlight_item is not None

def test_rule_dialog_extract_as_key_value_toggle(qapp):
    box = BoundingBox(x_pct=0.1, y_pct=0.2, width_pct=0.7, height_pct=0.4)
    dialog = RuleDialog(predefined_box=box)
    dialog.rule_type_combo.setCurrentText(RuleType.TABLE.value)
    dialog.key_name_input.setText("kv_table")
    dialog.data_type_combo.setCurrentText(DataType.STRING.value)
    
    assert dialog.table_as_kv_check.isChecked() is False
    dialog.table_as_kv_check.setChecked(True)
    
    rule = dialog._create_rule()
    assert isinstance(rule, TableExtractionRule)
    assert rule.config.extract_as_key_value is True
    
    # Check populate restores checkbox state
    dialog_edit = RuleDialog(rule=rule)
    assert dialog_edit.table_as_kv_check.isChecked() is True
