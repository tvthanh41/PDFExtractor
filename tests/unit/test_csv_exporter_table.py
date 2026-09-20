import json
import csv
import tempfile
import os
from src.domain.enums import DataType, ExtractionStatus
from src.domain.models import BoundingBox, ExtractedRecord, TableConfig, TableExtractionRule, Template
from src.services.csv_exporter import CSVExporter

def test_csv_exporter_serializes_table_as_json():
    rule = TableExtractionRule(
        key_name="items_table",
        data_type=DataType.STRING,
        box=BoundingBox(x_pct=0.1, y_pct=0.1, width_pct=0.5, height_pct=0.5),
        config=TableConfig()
    )
    template = Template(name="Invoice Template", rules=[rule])
    
    table_data = [
        ["Item", "Quantity", "Total"],
        ["Widget A", "2", "$20.00"],
        ["Widget B", "1", "$15.00"]
    ]
    
    record = ExtractedRecord(
        file_path="/tmp/test.pdf",
        file_name="test.pdf",
        extracted_values={"items_table": table_data},
        status=ExtractionStatus.SUCCESS
    )
    
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        csv_path = tf.name
        
    try:
        CSVExporter.export([record], template, csv_path)
        
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        assert len(rows) == 1
        raw_cell = rows[0]["items_table"]
        parsed_table = json.loads(raw_cell)
        assert parsed_table == table_data
        assert parsed_table[1][0] == "Widget A"
        assert parsed_table[2][2] == "$15.00"
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)
