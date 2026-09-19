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
