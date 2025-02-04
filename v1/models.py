from typing import Optional, List
from pydantic import BaseModel, Field

class Metric(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None

class Indicator(BaseModel):
    name: str
    assessment: Optional[str] = None
    metrics: Optional[Metric] = None

class Area(BaseModel):
    name: str
    assessment: Optional[str] = None
    indicators: List[Indicator] = Field(default_factory=list)

class Pillar(BaseModel):
    name: str
    areas: List[Area] = Field(default_factory=list)

class Metadata(BaseModel):
    country: str
    assessment_year: int

class ResponseData(BaseModel):
    metadata: Metadata
    pillars: List[Pillar] = Field(default_factory=list)

# Error handling models
class ErrorDetail(BaseModel):
    loc: List[str] = Field(description="Location of the error")
    msg: str = Field(description="Error message")
    type: str = Field(description="Error type")

class ErrorResponse(BaseModel):
    detail: List[ErrorDetail]

# Keep the original CountryData model for input validation
class CountryData(BaseModel):
    country: str
    assessment_year: int
    EP_1: str 
    EP_2: str
    EP_3: str
    CP_1: str
    CP_2: str
    CP_3: str
    CP_4: str
    CP_5: str
    CP_6: str
    CF_1: str
    CF_2: str
    CF_3: str
    CF_4: str