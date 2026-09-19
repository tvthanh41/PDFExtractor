from typing import Optional, List
import pymupdf as fitz
import re
from src.strategies.base import IExtractionStrategy
from src.domain.models import AnchorExtractionRule
from src.domain.enums import SearchMode, Direction
from src.services.pdf_service import PdfService

class AnchorExtractionStrategy(IExtractionStrategy):
    def __init__(self, rule: AnchorExtractionRule):
        self.rule = rule

    def extract(self, doc: fitz.Document, page_num: int) -> Optional[str]:
        if page_num < 0 or page_num >= len(doc):
            return None
            
        page = doc[page_num]
        words = page.get_text("words")
        
        anchor_rects = []
        if self.rule.search_mode in (SearchMode.EXACT, SearchMode.CONTAINS, SearchMode.CASE_INSENSITIVE):
            rects = page.search_for(self.rule.anchor_text)
            if self.rule.search_mode == SearchMode.CONTAINS:
                anchor_rects = rects
            else:
                for rect in rects:
                    intersecting = []
                    for w in words:
                        r = fitz.Rect(w[0], w[1], w[2], w[3])
                        
                        if r.height < 3: # Ignore microscopic artifacts
                            continue
                            
                        intersection = fitz.Rect(r)
                        intersection.intersect(rect)
                        
                        if not intersection.is_empty and (intersection.get_area() / rect.get_area() > 0.5 or intersection.get_area() / r.get_area() > 0.5):
                            intersecting.append((r.x0, w[4]))
                            
                    intersecting.sort(key=lambda x: x[0])
                    unique_words = []
                    last_x = -100
                    for m in intersecting:
                        if m[0] - last_x > 5:
                            unique_words.append(m[1])
                            last_x = m[0]
                            
                    joined_text = " ".join(unique_words)
                    
                    if self.rule.search_mode == SearchMode.CASE_INSENSITIVE:
                        if joined_text.strip().lower() == self.rule.anchor_text.strip().lower():
                            anchor_rects.append(rect)
                    else:
                        if joined_text.strip() == self.rule.anchor_text.strip():
                            anchor_rects.append(rect)
        else:
            # For REGEX, we iterate over lines to find a match
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:
                    for line in block.get("lines", []):
                        line_text = "".join([s["text"] for s in line.get("spans", [])])
                        try:
                            if bool(re.search(self.rule.anchor_text, line_text)):
                                anchor_rects.append(fitz.Rect(line["bbox"]))
                        except re.error:
                            pass

        if not anchor_rects:
            return None
            
        if self.rule.match_index >= len(anchor_rects):
            return None
            
        anchor = anchor_rects[self.rule.match_index]
        matching_words = []
        
        for w in words:
            r = fitz.Rect(w[0], w[1], w[2], w[3])
            
            if r.height < 3:
                continue
            
            # Skip words that are part of the anchor itself
            intersection = fitz.Rect(r)
            intersection.intersect(anchor)
            if not intersection.is_empty and (intersection.get_area() / r.get_area()) > 0.5:
                continue
                
            dist = float('inf')
            
            if self.rule.direction == Direction.RIGHT:
                overlap = max(0, min(r.y1, anchor.y1) - max(r.y0, anchor.y0))
                if overlap > 0.5 * anchor.height and r.x0 >= anchor.x1:
                    dist = r.x0 - anchor.x1
            elif self.rule.direction == Direction.LEFT:
                overlap = max(0, min(r.y1, anchor.y1) - max(r.y0, anchor.y0))
                if overlap > 0.5 * anchor.height and r.x1 <= anchor.x0:
                    dist = anchor.x0 - r.x1
            elif self.rule.direction == Direction.BELOW:
                if r.x1 > anchor.x0 and r.x0 < anchor.x1 and r.y0 >= anchor.y1:
                    dist = r.y0 - anchor.y1
            elif self.rule.direction == Direction.ABOVE:
                if r.x1 > anchor.x0 and r.x0 < anchor.x1 and r.y1 <= anchor.y0:
                    dist = anchor.y0 - r.y1

            if dist <= self.rule.offset_distance:
                if self.rule.direction in (Direction.RIGHT, Direction.LEFT):
                    matching_words.append((r.x0, w[4], r.y0))
                else:
                    matching_words.append((r.y0, r.x0, w[4]))
                    
        if not matching_words:
            return None
            
        if self.rule.direction in (Direction.RIGHT, Direction.LEFT):
            # Sort horizontally by Y (to respect line breaks), then X
            matching_words.sort(key=lambda x: (round(x[2] / 5.0) * 5, x[0]))
            return " ".join([m[1] for m in matching_words])
        else:
            # Sort by Y, then pick the closest Y line
            matching_words.sort(key=lambda x: x[0])
            closest_y = matching_words[0][0]
            line_words = [m for m in matching_words if abs(m[0] - closest_y) < 5]
            line_words.sort(key=lambda x: x[1])
            return " ".join([m[2] for m in line_words])
