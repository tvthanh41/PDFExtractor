from PySide6.QtCore import QObject, Signal, QThread
from src.services.batch_engine import BatchEngine
from src.services.csv_exporter import CSVExporter
from src.domain.models import BatchJob
from src.ui.batch_dialog import BatchDialog

class WorkerThread(QThread):
    progress_signal = Signal(int, int, int)
    finished_signal = Signal(list)
    
    def __init__(self, engine, job):
        super().__init__()
        self.engine = engine
        self.job = job
        
    def progress_callback(self, completed, total, failed):
        self.progress_signal.emit(completed, total, failed)
        
    def run(self):
        results = self.engine.run(self.job, self.progress_callback)
        self.finished_signal.emit(results)

class BatchController(QObject):
    def __init__(self, parent_view=None):
        super().__init__()
        self.parent_view = parent_view
        self.dialog = None
        self.engine = None
        self.worker = None
        self.job = None
        
    def start_batch(self, template_path: str, input_dir: str, output_csv_path: str):
        self.job = BatchJob(
            template_path=template_path,
            input_dir=input_dir,
            output_csv_path=output_csv_path
        )
        
        self.dialog = BatchDialog(self.parent_view)
        self.engine = BatchEngine()
        
        self.worker = WorkerThread(self.engine, self.job)
        self.worker.progress_signal.connect(self.dialog.update_progress)
        self.worker.finished_signal.connect(self.on_batch_finished)
        
        self.dialog.btn_cancel.clicked.connect(self.cancel_batch)
        
        self.worker.start()
        self.dialog.exec()
        
    def cancel_batch(self):
        if self.engine:
            self.engine.cancel()
            self.dialog.append_log("Cancellation requested, waiting for pending tasks...")
            self.dialog.btn_cancel.setEnabled(False)
            
    def on_batch_finished(self, results):
        if self.job.status != "CANCELLED":
            from src.services.template_repository import TemplateRepository
            template = TemplateRepository.load(self.job.template_path)
            CSVExporter.export(results, template, self.job.output_csv_path)
            self.dialog.append_log(f"Exported results to {self.job.output_csv_path}")
            
        self.dialog.processing_finished()
