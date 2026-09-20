import pytest
import pymupdf as fitz
from PySide6.QtWidgets import QApplication
from src.domain.enums import DataType, RuleType, TableStrategy
from src.domain.models import BoundingBox, TableConfig, TableExtractionRule
from src.strategies.table_strategy import TableExtractionStrategy
from src.ui.rule_preview_dialog import RulePreviewDialog

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def create_advanced_table_pdf() -> fitz.Document:
    doc = fitz.open()
    page = doc.new_page(width=600, height=800)
    # Draw table with borders
    page.draw_rect(fitz.Rect(50, 50, 450, 200), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(50, 100), fitz.Point(450, 100), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(200, 50), fitz.Point(200, 200), color=(0, 0, 0), width=1)
    
    page.insert_text(fitz.Point(60, 80), "Header1", fontsize=11)
    page.insert_text(fitz.Point(210, 80), "Header2", fontsize=11)
    page.insert_text(fitz.Point(60, 150), "Val1", fontsize=11)
    page.insert_text(fitz.Point(210, 150), "Val2", fontsize=11)
    return doc

def test_advanced_table_strategy_options():
    doc = create_advanced_table_pdf()
    box = BoundingBox(x_pct=0.08, y_pct=0.06, width_pct=0.7, height_pct=0.2)
    
    # Bordered with custom snap tolerance and explicit vertical strategy
    config = TableConfig(
        has_borders=True,
        vertical_strategy=TableStrategy.LINES,
        horizontal_strategy=TableStrategy.LINES,
        header_rows_count=1,
        snap_tolerance=4.0
    )
    rule = TableExtractionRule(
        key_name="adv_table",
        data_type=DataType.STRING,
        box=box,
        page_index=0,
        config=config
    )
    
    strategy = TableExtractionStrategy(rule)
    result = strategy.extract(doc, 0)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) >= 2
    row0_str = " ".join(result[0])
    assert "Header1" in row0_str
    assert "Header2" in row0_str

def test_rule_preview_dialog_table_rendering(qapp):
    table_data = [
        ["Col1", "Col2"],
        ["ValA", "ValB"]
    ]
    dialog = RulePreviewDialog("test_table", table_data)
    rendered = dialog.text_edit.toPlainText()
    assert "Col1" in rendered
    assert "Col2" in rendered
    assert "-+-" in rendered  # check header separator
    assert "ValA" in rendered

def test_rule_preview_dialog_dict_rendering(qapp):
    dict_data = {
        "Main character": "Daniel Radcliffe",
        "Sidekick 1": "Rupert Grint",
        "Sidekick 2": "Emma Watson"
    }
    dialog = RulePreviewDialog("characters", dict_data)
    rendered = dialog.text_edit.toPlainText()
    assert "Main character" in rendered
    assert "Daniel Radcliffe" in rendered
    assert "Sidekick 1" in rendered
    assert "Rupert Grint" in rendered
    assert "Sidekick 2" in rendered
    assert "Emma Watson" in rendered
