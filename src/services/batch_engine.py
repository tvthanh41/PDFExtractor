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
    """
    record = ExtractedRecord(
        file_path=file_path,
        file_name=os.path.basename(file_path)
    )
    
    try:
        doc = fitz.open(file_path)
        
        for rule in template.rules:
            strategy = ExtractionStrategyFactory.create(rule)
            
            # For MVP, assume we just check page 0 for Anchor, or use rule.page_index for Box
            page_num = 0
            if hasattr(rule, 'page_index'):
                page_num = rule.page_index
                
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
