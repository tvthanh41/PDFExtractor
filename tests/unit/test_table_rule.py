import json
import pytest
from pydantic import ValidationError
from src.domain.enums import DataType, RuleType, TableStrategy
from src.domain.models import BoundingBox, TableConfig, TableExtractionRule, Template

def test_table_config_defaults():
    config = TableConfig()
    assert config.has_borders is True
    assert config.vertical_strategy == TableStrategy.LINES
    assert config.horizontal_strategy == TableStrategy.LINES
    assert config.header_rows_count == 1
    assert config.snap_tolerance == 3.0

def test_table_config_validation():
    with pytest.raises(ValidationError):
        TableConfig(header_rows_count=-1)

    with pytest.raises(ValidationError):
        TableConfig(snap_tolerance=-0.5)

    custom = TableConfig(
        has_borders=False,
        vertical_strategy=TableStrategy.TEXT,
        horizontal_strategy=TableStrategy.EXPLICIT,
        header_rows_count=2,
        snap_tolerance=5.0
    )
    assert custom.has_borders is False
    assert custom.vertical_strategy == TableStrategy.TEXT
    assert custom.header_rows_count == 2

def test_table_extraction_rule_creation():
    box = BoundingBox(x_pct=0.1, y_pct=0.2, width_pct=0.8, height_pct=0.5)
    rule = TableExtractionRule(
        key_name="invoices_table",
        data_type=DataType.STRING,
        box=box
    )
    assert rule.rule_type == RuleType.TABLE
    assert rule.key_name == "invoices_table"
    assert rule.page_index == 0
    assert rule.config.has_borders is True
    assert rule.config.header_rows_count == 1

def test_table_rule_template_roundtrip():
    box = BoundingBox(x_pct=0.05, y_pct=0.15, width_pct=0.9, height_pct=0.6)
    rule = TableExtractionRule(
        key_name="items",
        data_type=DataType.STRING,
        page_index=1,
        box=box,
        config=TableConfig(has_borders=False, vertical_strategy=TableStrategy.TEXT)
    )
    template = Template(name="Invoice Template", rules=[rule])
    
    # JSON serialization and deserialization
    json_str = template.model_dump_json()
    loaded_template = Template.model_validate_json(json_str)

    assert len(loaded_template.rules) == 1
    loaded_rule = loaded_template.rules[0]
    assert isinstance(loaded_rule, TableExtractionRule)
    assert loaded_rule.key_name == "items"
    assert loaded_rule.page_index == 1
    assert loaded_rule.config.has_borders is False
    assert loaded_rule.config.vertical_strategy == TableStrategy.TEXT

def test_table_config_extract_as_key_value():
    config = TableConfig(extract_as_key_value=True)
    assert config.extract_as_key_value is True
    
    rule = TableExtractionRule(
        key_name="char_roles",
        data_type=DataType.STRING,
        box=BoundingBox(x_pct=0.1, y_pct=0.1, width_pct=0.5, height_pct=0.5),
        config=config
    )
    json_str = rule.model_dump_json()
    loaded = TableExtractionRule.model_validate_json(json_str)
    assert loaded.config.extract_as_key_value is True
