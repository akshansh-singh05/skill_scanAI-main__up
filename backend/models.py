from pydantic import BaseModel
from typing import List


class InterviewRequest(BaseModel):
    role: str
    resume_text: str


class AnswerSubmission(BaseModel):
    question: str
    answer: str
    difficulty: str


class HRSubmission(BaseModel):
    answer: str


class ReportResponse(BaseModel):
    resume_score: int
    technical_score: int
    hr_score: int
    overall_readiness: int
    improvement_list: List[str]
