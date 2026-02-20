from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

from services.report_generator import generate_final_report, get_score_breakdown_chart_data

router = APIRouter()


# Request models
class GenerateReportRequest(BaseModel):
    resume_score: int
    technical_score: int
    hr_score: int
    role: str = "SDE"
    resume_details: Optional[Dict] = None
    technical_details: Optional[Dict] = None
    hr_details: Optional[Dict] = None


class QuickReportRequest(BaseModel):
    resume_score: int
    technical_score: int
    hr_score: int


@router.post("/generate-report")
async def create_report(request: GenerateReportRequest):
    """
    Generate comprehensive final assessment report.
    
    - Calculates weighted overall score
    - Determines readiness level
    - Provides improvement checklist and action items
    """
    # Validate scores
    for score_name, score_val in [
        ("resume_score", request.resume_score),
        ("technical_score", request.technical_score),
        ("hr_score", request.hr_score)
    ]:
        if not 0 <= score_val <= 100:
            raise HTTPException(
                status_code=400,
                detail=f"{score_name} must be between 0 and 100"
            )
    
    # Validate role
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    # Generate report
    report = generate_final_report(
        resume_score=request.resume_score,
        technical_score=request.technical_score,
        hr_score=request.hr_score,
        resume_details=request.resume_details,
        technical_details=request.technical_details,
        hr_details=request.hr_details,
        role=request.role
    )
    
    # Add chart data
    report["chart_data"] = get_score_breakdown_chart_data(
        request.resume_score,
        request.technical_score,
        request.hr_score
    )
    
    return report


@router.post("/quick-report")
async def quick_report(request: QuickReportRequest):
    """
    Generate quick summary report with just scores.
    """
    # Validate scores
    for score_name, score_val in [
        ("resume_score", request.resume_score),
        ("technical_score", request.technical_score),
        ("hr_score", request.hr_score)
    ]:
        if not 0 <= score_val <= 100:
            raise HTTPException(
                status_code=400,
                detail=f"{score_name} must be between 0 and 100"
            )
    
    report = generate_final_report(
        resume_score=request.resume_score,
        technical_score=request.technical_score,
        hr_score=request.hr_score
    )
    
    return {
        "overall_readiness": report["overall_readiness"],
        "readiness_level": report["readiness_level"],
        "scores": report["scores"],
        "summary": report["summary"]
    }


@router.get("/chart-data")
async def get_chart_data(
    resume_score: int = 0,
    technical_score: int = 0,
    hr_score: int = 0
):
    """Get chart-ready visualization data."""
    return get_score_breakdown_chart_data(
        resume_score,
        technical_score,
        hr_score
    )
