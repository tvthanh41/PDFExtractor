import os
import json
import csv
import tempfile
import pymupdf as fitz
from src.domain.enums import DataType, ExtractionStatus, JobStatus
from src.domain.models import BatchJob, BoundingBox, TableConfig, TableExtractionRule, Template
from src.services.batch_engine import BatchEngine
from src.services.csv_exporter import CSVExporter
from src.services.template_repository import TemplateRepository

def test_batch_table_extraction_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Create a PDF with a table
        pdf_path = os.path.join(tmpdir, "invoice_001.pdf")
        doc = fitz.open()
        page = doc.new_page(width=600, height=800)
        page.draw_rect(fitz.Rect(100, 100, 400, 200), color=(0, 0, 0), width=1)
        page.draw_line(fitz.Point(100, 150), fitz.Point(400, 150), color=(0, 0, 0), width=1)
        page.draw_line(fitz.Point(250, 100), fitz.Point(250, 200), color=(0, 0, 0), width=1)
        page.insert_text(fitz.Point(120, 130), "Product", fontsize=11)
        page.insert_text(fitz.Point(270, 130), "Price", fontsize=11)
        page.insert_text(fitz.Point(120, 180), "Gizmo", fontsize=11)
        page.insert_text(fitz.Point(270, 180), "$99.00", fontsize=11)
        doc.save(pdf_path)
        doc.close()
        
        # 2. Create template with TableExtractionRule
        box = BoundingBox(x_pct=0.15, y_pct=0.10, width_pct=0.55, height_pct=0.20)
        rule = TableExtractionRule(
            key_name="line_items",
            data_type=DataType.STRING,
            box=box,
            page_index=0,
            config=TableConfig(has_borders=True)
        )
        template = Template(name="Batch Table Template", rules=[rule])
        tpl_path = os.path.join(tmpdir, "test.pdftpl")
        TemplateRepository.save(template, tpl_path)
        
        # 3. Run BatchEngine
        output_csv = os.path.join(tmpdir, "output.csv")
        job = BatchJob(
            template_path=tpl_path,
            input_dir=tmpdir,
            output_csv_path=output_csv
        )
        engine = BatchEngine(max_workers=1)
        results = engine.run(job, lambda c, t, f: None)
        
        assert len(results) == 1
        record = results[0]
        assert record.status == ExtractionStatus.SUCCESS
        assert "line_items" in record.extracted_values
        table_val = record.extracted_values["line_items"]
        assert isinstance(table_val, list)
        
        # 4. Export to CSV
        CSVExporter.export(results, template, output_csv)
        assert os.path.exists(output_csv)
        
        with open(output_csv, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        assert len(rows) == 1
        assert "line_items" in rows[0]
        json_table = json.loads(rows[0]["line_items"])
        assert isinstance(json_table, list)
        assert len(json_table) >= 2
