import pytest
from pydantic import ValidationError
from src.domain.models import AnchorExtractionRule
from src.domain.enums import DataType

def test_key_name_allows_spaces():
    # Should not raise ValidationError
    rule = AnchorExtractionRule(
        key_name="Your Score:",
        data_type=DataType.STRING,
        anchor_text="Your Score:"
    )
    assert rule.key_name == "Your Score:"

def test_key_name_strips_whitespace():
    rule = AnchorExtractionRule(
        key_name="  My Key  ",
        data_type=DataType.STRING,
        anchor_text="Anchor"
    )
    assert rule.key_name == "My Key"

def test_key_name_empty_fails():
    with pytest.raises(ValidationError):
        AnchorExtractionRule(
            key_name="   ",
            data_type=DataType.STRING,
            anchor_text="Anchor"
        )
