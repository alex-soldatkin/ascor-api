from typing import List, Optional
from pydantic import BaseModel

class Metric(BaseModel):
    name: str
    value: Optional[str] = None

class Indicator(BaseModel):
    name: str
    assessment: Optional[str] = None
    metrics: Optional[Metric] = None

class Area(BaseModel):
    name: str
    assessment: Optional[str] = None
    indicators: List[Indicator] = []

class Pillar(BaseModel):
    name: str
    areas: List[Area] = []

class Metadata(BaseModel):
    country: str
    assessment_year: int

class ResponseData(BaseModel):
    metadata: Metadata
    pillars: List[Pillar] = []

class ErrorResponse(BaseModel):
    message: str
    details: dict = {}
