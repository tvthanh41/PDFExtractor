import os
import tempfile
import json
import pytest

from src.domain.models import Template
from src.domain.enums import DataType, RuleType, SearchMode, Direction
from src.domain.models import AnchorExtractionRule
from src.services.template_repository import TemplateRepository


def _make_template(name: str) -> Template:
    return Template(name=name, rules=[
        AnchorExtractionRule(
            key_name="total",
            data_type=DataType.CURRENCY,
            anchor_text="Total:",
            search_mode=SearchMode.EXACT,
            direction=Direction.RIGHT,
            offset_distance=200.0
        )
    ])


def test_load_uses_name_from_json():
    """Loading a template should return the name stored in the JSON, not the filename."""
    template = _make_template("My Custom Name")

    with tempfile.NamedTemporaryFile(suffix=".pdftpl", delete=False, mode='w') as f:
        f.write(template.model_dump_json())
        tmp_path = f.name

    try:
        loaded = TemplateRepository.load(tmp_path)
        # Should use the JSON's stored name, not the random tmpfile name
        assert loaded.name == "My Custom Name"
    finally:
        os.unlink(tmp_path)


def test_save_syncs_template_name_to_filename():
    """Saving a template should update the in-memory template name to match the filename."""
    template = _make_template("Old Name")

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "my_saved_template.pdftpl")
        TemplateRepository.save(template, save_path)

        # The in-memory template name should be updated
        assert template.name == "my_saved_template"

        # The file should also persist the correct name
        with open(save_path, 'r') as f:
            data = json.load(f)
        assert data["name"] == "my_saved_template"


def test_round_trip_preserves_correct_name():
    """Save then load should yield the filename-based name (set during save), read back from JSON."""
    original = _make_template("Whatever Name")

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "invoice_v2.pdftpl")
        TemplateRepository.save(original, save_path)
        loaded = TemplateRepository.load(save_path)

        # save() wrote "invoice_v2" into the JSON, load() reads it back
        assert loaded.name == "invoice_v2"

