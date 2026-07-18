from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str = Field(..., description="User's natural language question")


class SourceChunk(BaseModel):
    document: str
    page: Optional[int] = None
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk] = []


class PremiumRequest(BaseModel):
    age: int = Field(..., gt=0, lt=100)
    sum_assured: float = Field(..., gt=0, description="Total insured amount")
    term_years: int = Field(..., gt=0, le=50)
    plan_type: str = Field("term", description="term | endowment | health")
    smoker: bool = False


class PremiumResponse(BaseModel):
    estimated_annual_premium: float
    estimated_monthly_premium: float
    risk_loading_applied: float
    breakdown: dict


class CompareRequest(BaseModel):
    questions: List[str]
    policy_names: Optional[List[str]] = None


class CompareResponse(BaseModel):
    comparison: List[ChatResponse]


class DocumentInfo(BaseModel):
    filename: str
    chunks_indexed: int


class UploadResponse(BaseModel):
    message: str
    documents: List[DocumentInfo]
