from typing import Optional
import pymupdf as fitz
from src.strategies.base import IExtractionStrategy
from src.domain.models import BoundingBoxExtractionRule
from src.services.pdf_service import PdfService

class BoundingBoxExtractionStrategy(IExtractionStrategy):
    def __init__(self, rule: BoundingBoxExtractionRule):
        self.rule = rule

    def extract(self, doc: fitz.Document, page_num: int) -> Optional[str]:
        # BoundingBoxExtractionRule has its own page_index
        # Use that instead of the page_num passed from iteration if needed,
        # but typically the engine will pass the rule.page_index here.
        if page_num != self.rule.page_index:
            return None
            
        page = doc[page_num]
        page_x0, page_y0, width, height = PdfService.get_page_dimensions(doc, page_num)
        
        # Convert percentages to points, accounting for CropBox offset
        x0 = page_x0 + self.rule.box.x_pct * width
        y0 = page_y0 + self.rule.box.y_pct * height
        x1 = x0 + (self.rule.box.width_pct * width)
        y1 = y0 + (self.rule.box.height_pct * height)
        
        target_rect = fitz.Rect(x0, y0, x1, y1)
        
        # Get text that falls inside the rectangle
        # Using simple get_text("text", clip=...) for bounding box
        text = page.get_text("text", clip=target_rect)
        if text:
            # Simple deduplication for fake bolding artifacts
            lines = text.strip().split('\n')
            deduped = []
            for line in lines:
                if not deduped or line != deduped[-1]:
                    deduped.append(line)
            return '\n'.join(deduped)
            
        return None
