import os
import pytest
from src.services.batch_engine import BatchEngine
from src.domain.models import BatchJob, Template, AnchorExtractionRule, DataType
from src.domain.enums import SearchMode, Direction
from src.services.template_repository import TemplateRepository
import fitz

@pytest.fixture
def temp_workspace(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    
    output_csv = tmp_path / "output.csv"
    template_path = tmp_path / "test.pdftpl"
    
    # Create sample PDF
    pdf_path = input_dir / "sample1.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(fitz.Point(50, 50), "Total: $500")
    doc.save(str(pdf_path))
    doc.close()
    
    # Create template
    rule = AnchorExtractionRule(
        key_name="total_amount",
        data_type=DataType.STRING,
        anchor_text="Total:",
        search_mode=SearchMode.EXACT,
        direction=Direction.RIGHT
    )
    template = Template(name="Test Template", rules=[rule])
    TemplateRepository.save(template, str(template_path))
    
    return str(input_dir), str(template_path), str(output_csv)

def test_batch_engine_processes_files(temp_workspace):
    input_dir, template_path, output_csv = temp_workspace
    
    job = BatchJob(
        template_path=template_path,
        input_dir=input_dir,
        output_csv_path=output_csv
    )
    
    engine = BatchEngine(max_workers=1)
    
    # Progress callback mock
    progress_calls = []
    def callback(c, t, f):
        progress_calls.append((c, t, f))
        
    results = engine.run(job, callback)
    
    assert len(results) == 1
    assert results[0].file_name == "sample1.pdf"
    assert "total_amount" in results[0].extracted_values
    
    assert len(progress_calls) == 1
    assert progress_calls[0] == (1, 1, 0)
    
    assert job.status.value == "COMPLETED"
    assert job.processed_files == 1
