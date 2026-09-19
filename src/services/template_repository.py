import json
import os
from src.domain.models import Template

class TemplateRepository:

    @staticmethod
    def load(file_path: str) -> Template:
        """
        Loads a Template from a .pdftpl JSON file.
        The template name is read directly from the JSON content.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Template.model_validate(data)

    @staticmethod
    def save(template: Template, file_path: str) -> None:
        """
        Serializes a Template to JSON and saves it to a .pdftpl file.
        Updates the template's name to the file's basename before writing,
        so the stored name always matches the filename.
        """
        template.name = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template.model_dump_json(indent=2))
