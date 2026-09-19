import uuid
from datetime import datetime, timezone
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field, constr
from .enums import DataType, RuleType, SearchMode, Direction, JobStatus, ExtractionStatus

class BoundingBox(BaseModel):
    x_pct: float = Field(..., ge=0.0, le=1.0)
    y_pct: float = Field(..., ge=0.0, le=1.0)
    width_pct: float = Field(..., ge=0.0, le=1.0)
    height_pct: float = Field(..., ge=0.0, le=1.0)

class ExtractionRuleBase(BaseModel):
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key_name: constr(min_length=1, strip_whitespace=True) # type: ignore
    data_type: DataType
    rule_type: RuleType

class AnchorExtractionRule(ExtractionRuleBase):
    rule_type: RuleType = RuleType.ANCHOR_SEARCH
    anchor_text: str
    search_mode: SearchMode = SearchMode.EXACT
    direction: Direction = Direction.RIGHT
    offset_distance: float = Field(default=150.0, ge=0)
    match_index: int = Field(default=0, ge=0)

class BoundingBoxExtractionRule(ExtractionRuleBase):
    rule_type: RuleType = RuleType.BOUNDING_BOX
    page_index: int = Field(default=0, ge=0)
    box: BoundingBox

ExtractionRule = Union[AnchorExtractionRule, BoundingBoxExtractionRule]

class Template(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: constr(min_length=1, max_length=100) # type: ignore
    description: Optional[constr(max_length=500)] = "" # type: ignore
    version: constr(pattern=r"^\d+\.\d+\.\d+$") = "1.0.0" # type: ignore
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rules: List[ExtractionRule] = Field(default_factory=list)

class ExtractedRecord(BaseModel):
    file_path: str
    file_name: str
    extracted_values: Dict[str, Any] = Field(default_factory=dict)
    status: ExtractionStatus = ExtractionStatus.SUCCESS
    error_message: Optional[str] = None

class BatchJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_path: str
    input_dir: str
    output_csv_path: str
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    status: JobStatus = JobStatus.PENDING
    logs: List[str] = Field(default_factory=list)
