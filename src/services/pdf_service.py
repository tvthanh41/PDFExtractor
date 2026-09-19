import pymupdf as fitz
from typing import List, Dict, Any, Tuple

class PdfService:
    @staticmethod
    def load_document(file_path: str) -> fitz.Document:
        """
        Loads a PDF document from a given file path.
        """
        return fitz.open(file_path)

    @staticmethod
    def get_text_blocks(doc: fitz.Document, page_num: int) -> List[Dict[str, Any]]:
        """
        Extracts text blocks with their coordinates from a specific page.
        
        Returns a list of blocks, where each block is a dictionary 
        containing bounding box and text content.
        Uses fitz page.get_text("blocks").
        """
        if page_num < 0 or page_num >= len(doc):
            return []
            
        page = doc[page_num]
        # blocks format: (x0, y0, x1, y1, "lines in block", block_no, block_type)
        # block_type 0 means text
        raw_blocks = page.get_text("blocks")
        
        blocks = []
        for b in raw_blocks:
            if b[6] == 0:  # text block
                blocks.append({
                    "rect": fitz.Rect(b[0], b[1], b[2], b[3]),
                    "text": b[4].strip()
                })
        return blocks
        
    @staticmethod
    def get_page_dimensions(doc: fitz.Document, page_num: int) -> Tuple[float, float, float, float]:
        """
        Returns (x0, y0, width, height) of the page in points.
        """
        if page_num < 0 or page_num >= len(doc):
            return (0.0, 0.0, 0.0, 0.0)
            
        page = doc[page_num]
        return page.rect.x0, page.rect.y0, page.rect.width, page.rect.height
