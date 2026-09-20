import pytest
import pymupdf as fitz
from src.domain.enums import DataType, RuleType, TableStrategy
from src.domain.models import BoundingBox, TableConfig, TableExtractionRule
from src.strategies.table_strategy import TableExtractionStrategy
from src.strategies.factory import ExtractionStrategyFactory

def create_table_pdf() -> fitz.Document:
    doc = fitz.open()
    page = doc.new_page(width=600, height=800)
    
    # Draw simple table grid at (100, 100) to (400, 250)
    # Header: Item | Price
    # Row 1: Apple | $1.00
    # Row 2: Orange | $2.00
    # Outer rect
    page.draw_rect(fitz.Rect(100, 100, 400, 250), color=(0, 0, 0), width=1)
    # Horizontal lines
    page.draw_line(fitz.Point(100, 150), fitz.Point(400, 150), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(100, 200), fitz.Point(400, 200), color=(0, 0, 0), width=1)
    # Vertical line
    page.draw_line(fitz.Point(250, 100), fitz.Point(250, 250), color=(0, 0, 0), width=1)
    
    # Text
    page.insert_text(fitz.Point(120, 130), "Item", fontsize=11)
    page.insert_text(fitz.Point(270, 130), "Price", fontsize=11)
    page.insert_text(fitz.Point(120, 180), "Apple", fontsize=11)
    page.insert_text(fitz.Point(270, 180), "$1.00", fontsize=11)
    page.insert_text(fitz.Point(120, 230), "Orange", fontsize=11)
    page.insert_text(fitz.Point(270, 230), "$2.00", fontsize=11)
    
    return doc

def test_table_strategy_extraction():
    doc = create_table_pdf()
    
    # Table box is in (100, 100) -> (400, 250)
    # x_pct: 100/600 = 0.1666, y_pct: 100/800 = 0.125
    # w_pct: 300/600 = 0.5, h_pct: 150/800 = 0.1875
    box = BoundingBox(x_pct=0.15, y_pct=0.10, width_pct=0.55, height_pct=0.25)
    rule = TableExtractionRule(
        key_name="items",
        data_type=DataType.STRING,
        box=box,
        page_index=0,
        config=TableConfig(has_borders=True)
    )
    
    strategy = ExtractionStrategyFactory.create(rule)
    assert isinstance(strategy, TableExtractionStrategy)
    
    result = strategy.extract(doc, 0)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) >= 2
    # First row should have Item and Price
    first_row_str = " ".join(str(c) for c in result[0])
    assert "Item" in first_row_str
    assert "Price" in first_row_str

def test_table_strategy_wrong_page():
    doc = create_table_pdf()
    box = BoundingBox(x_pct=0.15, y_pct=0.10, width_pct=0.55, height_pct=0.25)
    rule = TableExtractionRule(
        key_name="items",
        data_type=DataType.STRING,
        box=box,
        page_index=1,
        config=TableConfig()
    )
    strategy = TableExtractionStrategy(rule)
    assert strategy.extract(doc, 0) is None

def test_table_strategy_extract_as_key_value():
    doc = fitz.open()
    page = doc.new_page(width=600, height=800)
    
    # 2-column key-value table matching user's image
    # Row 0: Main character | Daniel Radcliffe
    # Row 1: Sidekick 1     | Rupert Grint
    # Row 2: Sidekick 2     | Emma Watson
    page.draw_rect(fitz.Rect(50, 50, 500, 200), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(50, 100), fitz.Point(500, 100), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(50, 150), fitz.Point(500, 150), color=(0, 0, 0), width=1)
    page.draw_line(fitz.Point(220, 50), fitz.Point(220, 200), color=(0, 0, 0), width=1)
    
    page.insert_text(fitz.Point(60, 85), "Main character", fontsize=11)
    page.insert_text(fitz.Point(230, 85), "Daniel Radcliffe", fontsize=11)
    page.insert_text(fitz.Point(60, 135), "Sidekick 1", fontsize=11)
    page.insert_text(fitz.Point(230, 135), "Rupert Grint", fontsize=11)
    page.insert_text(fitz.Point(60, 185), "Sidekick 2", fontsize=11)
    page.insert_text(fitz.Point(230, 185), "Emma Watson", fontsize=11)
    
    box = BoundingBox(x_pct=0.05, y_pct=0.05, width_pct=0.8, height_pct=0.25)
    rule = TableExtractionRule(
        key_name="cast_info",
        data_type=DataType.STRING,
        box=box,
        page_index=0,
        config=TableConfig(has_borders=True, extract_as_key_value=True)
    )
    
    strategy = TableExtractionStrategy(rule)
    result = strategy.extract(doc, 0)
    
    assert isinstance(result, dict)
    assert "Main character" in result
    assert "Daniel Radcliffe" in result["Main character"]
    assert "Sidekick 1" in result
    assert "Rupert Grint" in result["Sidekick 1"]
    assert "Sidekick 2" in result
    assert "Emma Watson" in result["Sidekick 2"]
