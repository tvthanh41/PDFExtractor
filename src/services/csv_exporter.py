import csv
import json
import os
from typing import List
from src.domain.models import ExtractedRecord, Template

class CSVExporter:
    @staticmethod
    def export(records: List[ExtractedRecord], template: Template, output_path: str):
        if not records:
            return
            
        import datetime, getpass
            
        # Define header
        # Custom fields from rules + metadata
        rule_keys = [r.key_name for r in template.rules]
        headers = ["file name", "file path", "generated time", "user", "template name", "_status", "_error_message"] + rule_keys
        
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            
            for record in records:
                row = {
                    "file name": record.file_name,
                    "file path": record.file_path,
                    "generated time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "template name": template.name,
                    "_status": record.status.value,
                    "_error_message": record.error_message or ""
                }
                try:
                    row["user"] = getpass.getuser()
                except Exception:
                    row["user"] = "Unknown"
                
                # Fill in extracted data
                for key in rule_keys:
                    val = record.extracted_values.get(key, "")
                    if isinstance(val, (list, dict)):
                        row[key] = json.dumps(val, ensure_ascii=False)
                    else:
                        row[key] = val if val is not None else ""
                    
                writer.writerow(row)
