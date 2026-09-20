"""
Unit tests for updated domain models (multi-page/pattern table feature).
Validates Pydantic serialization, defaults, and backward compatibility.
"""
import pytest
from src.domain.enums import TableBoundaryType, TableEngine, RuleType
from src.domain.models import (
    PatternBoundaryConfig,
    AnchorExtractionRule,
    BoundingBox,
    BoundingBoxExtractionRule,
    TableConfig,
    TableExtractionRule,
    Template,
)


# ---------------------------------------------------------------------------
# PatternBoundaryConfig
# ---------------------------------------------------------------------------

class TestPatternBoundaryConfig:
    def test_defaults(self):
        cfg = PatternBoundaryConfig(start_pattern="Header", end_pattern="Total")
        assert cfg.include_start is True
        assert cfg.include_end is False
        assert cfg.is_regex is False
        assert cfg.skip_k == 0

    def test_custom_values(self):
        cfg = PatternBoundaryConfig(
            start_pattern=r"\bItem\b",
            end_pattern=r"\bSubtotal\b",
            include_start=False,
            include_end=True,
            is_regex=True,
            skip_k=2,
        )
        assert cfg.skip_k == 2
        assert cfg.is_regex is True
        assert cfg.include_end is True

    def test_skip_k_must_be_non_negative(self):
        with pytest.raises(Exception):
            PatternBoundaryConfig(start_pattern="A", end_pattern="B", skip_k=-1)

    def test_empty_start_pattern_invalid(self):
        with pytest.raises(Exception):
            PatternBoundaryConfig(start_pattern="", end_pattern="Total")

    def test_roundtrip_json(self):
        cfg = PatternBoundaryConfig(start_pattern="Header", end_pattern="Footer", skip_k=1)
        restored = PatternBoundaryConfig.model_validate_json(cfg.model_dump_json())
        assert restored.start_pattern == "Header"
        assert restored.skip_k == 1


# ---------------------------------------------------------------------------
# AnchorExtractionRule — backward compat + new page_index field
# ---------------------------------------------------------------------------

class TestAnchorExtractionRuleUpdated:
    def test_default_page_index(self):
        rule = AnchorExtractionRule(
            key_name="invoice_date",
            data_type="STRING",
            anchor_text="Date:",
        )
        assert rule.page_index == 0
        assert rule.rule_type == RuleType.ANCHOR_SEARCH

    def test_custom_page_index(self):
        rule = AnchorExtractionRule(
            key_name="ref",
            data_type="STRING",
            anchor_text="Ref:",
            page_index=3,
        )
        assert rule.page_index == 3

    def test_page_index_non_negative(self):
        with pytest.raises(Exception):
            AnchorExtractionRule(
                key_name="x",
                data_type="STRING",
                anchor_text="Y",
                page_index=-1,
            )

    def test_match_index_skip_k_equivalence(self):
        """match_index is the existing field that acts as skip_k."""
        rule = AnchorExtractionRule(
            key_name="total",
            data_type="STRING",
            anchor_text="Total:",
            match_index=2,
        )
        assert rule.match_index == 2

    def test_roundtrip_json(self):
        rule = AnchorExtractionRule(
            key_name="total",
            data_type="STRING",
            anchor_text="Total:",
            page_index=1,
            match_index=1,
        )
        data = rule.model_dump_json()
        restored = AnchorExtractionRule.model_validate_json(data)
        assert restored.page_index == 1
        assert restored.match_index == 1
        assert restored.anchor_text == "Total:"


# ---------------------------------------------------------------------------
# TableConfig — engine field
# ---------------------------------------------------------------------------

class TestTableConfigEngine:
    def test_default_engine(self):
        cfg = TableConfig()
        assert cfg.engine == TableEngine.PYMUPDF

    def test_pymupdf4llm_engine(self):
        cfg = TableConfig(engine=TableEngine.PYMUPDF4LLM)
        assert cfg.engine == TableEngine.PYMUPDF4LLM

    def test_roundtrip_json(self):
        cfg = TableConfig(engine=TableEngine.PYMUPDF4LLM, extract_as_key_value=True)
        restored = TableConfig.model_validate_json(cfg.model_dump_json())
        assert restored.engine == TableEngine.PYMUPDF4LLM


# ---------------------------------------------------------------------------
# TableExtractionRule — boundary_type, optional box, pattern_boundary
# ---------------------------------------------------------------------------

class TestTableExtractionRuleUpdated:
    def test_default_boundary_type(self):
        box = BoundingBox(x_pct=0.1, y_pct=0.1, width_pct=0.5, height_pct=0.3)
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            box=box,
        )
        assert rule.boundary_type == TableBoundaryType.BOUNDING_BOX
        assert rule.pattern_boundary is None

    def test_pattern_match_boundary_type(self):
        pb = PatternBoundaryConfig(start_pattern="Item Description", end_pattern="Subtotal")
        rule = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.PATTERN_MATCH,
            pattern_boundary=pb,
        )
        assert rule.boundary_type == TableBoundaryType.PATTERN_MATCH
        assert rule.box is None
        assert rule.pattern_boundary.start_pattern == "Item Description"

    def test_page_index_default(self):
        box = BoundingBox(x_pct=0, y_pct=0, width_pct=1, height_pct=1)
        rule = TableExtractionRule(key_name="t", data_type="STRING", box=box)
        assert rule.page_index == 0

    def test_backwards_compat_box_only(self):
        """Existing templates with only 'box' should still load."""
        import json
        legacy_data = {
            "rule_id": "abc",
            "key_name": "legacy_table",
            "data_type": "STRING",
            "rule_type": "TABLE",
            "page_index": 0,
            "box": {"x_pct": 0.0, "y_pct": 0.1, "width_pct": 0.9, "height_pct": 0.5},
            "config": {
                "has_borders": True,
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "header_rows_count": 1,
                "snap_tolerance": 3.0,
                "extract_as_key_value": False,
            },
        }
        rule = TableExtractionRule.model_validate(legacy_data)
        assert rule.key_name == "legacy_table"
        assert rule.box.x_pct == 0.0
        assert rule.boundary_type == TableBoundaryType.BOUNDING_BOX
        assert rule.config.engine == TableEngine.PYMUPDF

    def test_roundtrip_pattern_rule(self):
        pb = PatternBoundaryConfig(start_pattern="Header", end_pattern="Footer", skip_k=1)
        rule = TableExtractionRule(
            key_name="tbl",
            data_type="STRING",
            boundary_type=TableBoundaryType.PATTERN_MATCH,
            pattern_boundary=pb,
        )
        restored = TableExtractionRule.model_validate_json(rule.model_dump_json())
        assert restored.pattern_boundary.skip_k == 1
        assert restored.boundary_type == TableBoundaryType.PATTERN_MATCH


# ---------------------------------------------------------------------------
# Template round-trip with mixed rule types
# ---------------------------------------------------------------------------

class TestTemplateMixedRules:
    def test_template_with_anchor_and_pattern_table(self):
        anchor = AnchorExtractionRule(
            key_name="date", data_type="STRING", anchor_text="Date:", page_index=0
        )
        pb = PatternBoundaryConfig(start_pattern="Item", end_pattern="Total")
        table = TableExtractionRule(
            key_name="items",
            data_type="STRING",
            boundary_type=TableBoundaryType.PATTERN_MATCH,
            pattern_boundary=pb,
            page_index=1,
        )
        template = Template(name="Test Template", rules=[anchor, table])
        restored = Template.model_validate_json(template.model_dump_json())
        assert len(restored.rules) == 2
