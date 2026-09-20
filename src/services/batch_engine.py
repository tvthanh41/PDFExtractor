import os
import concurrent.futures
from typing import List, Callable, Optional
import pymupdf as fitz
from src.domain.models import ExtractedRecord, Template, BatchJob
from src.domain.enums import JobStatus, ExtractionStatus
from src.strategies.factory import ExtractionStrategyFactory
from src.services.template_repository import TemplateRepository

def process_file_worker(file_path: str, template: Template) -> ExtractedRecord:
    """
    Standalone function to process a single PDF file (GIL-friendly).
    Each rule is executed on its specified page_index (0-indexed).
    If page_index exceeds the document's page count, the rule result is None.
    """
    record = ExtractedRecord(
        file_path=file_path,
        file_name=os.path.basename(file_path)
    )
    
    try:
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        for rule in template.rules:
            page_num = getattr(rule, 'page_index', 0)
            if page_num >= total_pages:
                record.extracted_values[rule.key_name] = None
                continue
                
            strategy = ExtractionStrategyFactory.create(rule)
            val = strategy.extract(doc, page_num)
            record.extracted_values[rule.key_name] = val
            
        record.status = ExtractionStatus.SUCCESS
        doc.close()
        
    except Exception as e:
        record.status = ExtractionStatus.FAILED
        record.error_message = str(e)
        
    return record

class BatchEngine:
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers
        self.is_cancelled = False
        
    def cancel(self):
        self.is_cancelled = True
        
    def run(self, job: BatchJob, 
            progress_callback: Callable[[int, int, int], None]) -> List[ExtractedRecord]:
            
        template = TemplateRepository.load(job.template_path)
        
        # Find all pdfs recursively
        pdf_files = []
        for root, _, files in os.walk(job.input_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
                    
        job.total_files = len(pdf_files)
        job.status = JobStatus.RUNNING
        
        results = []
        completed = 0
        failed = 0
        
        if not pdf_files:
            job.status = JobStatus.COMPLETED
            return []
            
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            future_to_pdf = {
                executor.submit(process_file_worker, pdf, template): pdf 
                for pdf in pdf_files
            }
            
            for future in concurrent.futures.as_completed(future_to_pdf):
                if self.is_cancelled:
                    executor.shutdown(wait=False, cancel_futures=True)
                    job.status = JobStatus.CANCELLED
                    break
                    
                record = future.result()
                results.append(record)
                
                if record.status == ExtractionStatus.FAILED:
                    failed += 1
                completed += 1
                
                if progress_callback:
                    progress_callback(completed, job.total_files, failed)
                    
        if not self.is_cancelled:
            job.status = JobStatus.COMPLETED
            job.processed_files = completed
            job.failed_files = failed
            
        return results
