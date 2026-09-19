from abc import ABC, abstractmethod
from typing import Optional
import pymupdf as fitz  # PyMuPDF

class IExtractionStrategy(ABC):
    """
    Abstract strategy interface for extracting text from a PDF page.
    """
    @abstractmethod
    def extract(self, doc: fitz.Document, page_num: int) -> Optional[str]:
        """
        Extract text from the specified page of the document.
        
        Args:
            doc: The PyMuPDF document instance.
            page_num: 0-indexed page number to extract from.
            
        Returns:
            The extracted text string, or None if the rule didn't match anything.
        """
        pass
