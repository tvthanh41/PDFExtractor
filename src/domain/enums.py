from enum import Enum

class DataType(str, Enum):
    STRING = "STRING"
    NUMBER = "NUMBER"
    CURRENCY = "CURRENCY"
    DATE = "DATE"

class SearchMode(str, Enum):
    EXACT = "EXACT"
    CONTAINS = "CONTAINS"
    REGEX = "REGEX"
    CASE_INSENSITIVE = "CASE_INSENSITIVE"

class Direction(str, Enum):
    RIGHT = "RIGHT"
    BELOW = "BELOW"
    LEFT = "LEFT"
    ABOVE = "ABOVE"

class RuleType(str, Enum):
    ANCHOR_SEARCH = "ANCHOR_SEARCH"
    BOUNDING_BOX = "BOUNDING_BOX"
    TABLE = "TABLE"

class TableStrategy(str, Enum):
    LINES = "lines"
    TEXT = "text"
    EXPLICIT = "explicit"

class TableBoundaryType(str, Enum):
    BOUNDING_BOX = "BOUNDING_BOX"
    PATTERN_MATCH = "PATTERN_MATCH"

class TableEngine(str, Enum):
    PYMUPDF = "pymupdf"
    PYMUPDF4LLM = "pymupdf4llm"

class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class ExtractionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
