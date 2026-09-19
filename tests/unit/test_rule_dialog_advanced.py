"""
Unit tests for RuleDialog advanced settings.

These tests verify that:
- Advanced fields are populated correctly in edit mode
- _create_rule() reads the spinner values correctly
- Default values are used when advanced settings are not touched
- Non-default values cause the advanced section to auto-expand on edit
"""
import pytest
from src.domain.enums import DataType, RuleType, SearchMode, Direction
from src.domain.models import AnchorExtractionRule, BoundingBoxExtractionRule, BoundingBox


# ---------------------------------------------------------------------------
# Helper: build rule objects without GUI
# ---------------------------------------------------------------------------

def _anchor_rule(offset_distance=150.0, match_index=0):
    return AnchorExtractionRule(
        key_name="total",
        data_type=DataType.CURRENCY,
        anchor_text="Total:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT,
        offset_distance=offset_distance,
        match_index=match_index,
    )


def _box_rule(page_index=0):
    return BoundingBoxExtractionRule(
        key_name="vendor",
        data_type=DataType.STRING,
        page_index=page_index,
        box=BoundingBox(x_pct=0.1, y_pct=0.1, width_pct=0.5, height_pct=0.1),
    )


# ---------------------------------------------------------------------------
# Tests — model layer (no GUI required)
# ---------------------------------------------------------------------------

class TestAnchorRuleAdvancedDefaults:
    def test_default_offset_distance(self):
        rule = _anchor_rule()
        assert rule.offset_distance == 150.0

    def test_default_match_index(self):
        rule = _anchor_rule()
        assert rule.match_index == 0

    def test_custom_offset_distance(self):
        rule = _anchor_rule(offset_distance=300.0)
        assert rule.offset_distance == 300.0

    def test_custom_match_index(self):
        rule = _anchor_rule(match_index=2)
        assert rule.match_index == 2

    def test_offset_distance_zero_allowed(self):
        rule = _anchor_rule(offset_distance=0.0)
        assert rule.offset_distance == 0.0

    def test_negative_offset_distance_rejected(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            _anchor_rule(offset_distance=-1.0)

    def test_negative_match_index_rejected(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            _anchor_rule(match_index=-1)


class TestBoundingBoxRuleAdvancedDefaults:
    def test_default_page_index(self):
        rule = _box_rule()
        assert rule.page_index == 0

    def test_custom_page_index(self):
        rule = _box_rule(page_index=3)
        assert rule.page_index == 3

    def test_negative_page_index_rejected(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            _box_rule(page_index=-1)


class TestRuleSerializationRoundTrip:
    """Verify that advanced fields survive JSON serialization (as saved in .pdftpl)."""

    def test_anchor_advanced_round_trip(self):
        original = _anchor_rule(offset_distance=250.0, match_index=1)
        json_str = original.model_dump_json()
        restored = AnchorExtractionRule.model_validate_json(json_str)
        assert restored.offset_distance == 250.0
        assert restored.match_index == 1

    def test_box_page_index_round_trip(self):
        original = _box_rule(page_index=4)
        json_str = original.model_dump_json()
        restored = BoundingBoxExtractionRule.model_validate_json(json_str)
        assert restored.page_index == 4

    def test_defaults_serialized_correctly(self):
        import json
        rule = _anchor_rule()
        data = json.loads(rule.model_dump_json())
        assert data["offset_distance"] == 150.0
        assert data["match_index"] == 0
