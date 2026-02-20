from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from services.resume_parser import extract_text_from_pdf
from services.ats_scorer import calculate_ats_score
from services.skill_gap_analyzer import analyze_skill_gaps
from services.bullet_improver import improve_bullet, batch_improve_bullets
from services.career_recommender import analyze_career_fit, get_career_path_details, get_all_career_paths

router = APIRouter()


class BulletImproveRequest(BaseModel):
    bullet: str
    role: str = "SDE"


class BatchBulletRequest(BaseModel):
    bullets: List[str]
    role: str = "SDE"


class CareerAnalysisRequest(BaseModel):
    resume_text: str
    skills: List[str] = []


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(default="SDE")
):
    """
    Upload resume PDF and get ATS analysis.
    
    - Accepts PDF file and target role
    - Parses resume text
    - Calculates ATS score
    - Returns score and missing skills
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Validate role
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    # Parse resume
    resume_text = await extract_text_from_pdf(file)
    
    # Calculate ATS score
    ats_result = calculate_ats_score(resume_text, role)
    
    # Get skill gap analysis
    skill_gaps = analyze_skill_gaps(resume_text, role)
    
    return {
        "filename": file.filename,
        "role": role,
        "resume_text": resume_text,
        "ats_score": ats_result["ats_score"],
        "missing_skills": ats_result["missing_skills"],
        "weak_areas": ats_result["weak_areas"],
        "suggestions": ats_result["suggestions"],
        "matched_skills": ats_result["matched_skills"],
        "skill_match": {
            "core": ats_result["core_match"],
            "advanced": ats_result["advanced_match"]
        },
        "skill_gaps": {
            "match_percentage": skill_gaps["skill_match_percentage"],
            "priority_improvements": skill_gaps["priority_improvement_order"][:5]
        }
    }


@router.post("/analyze")
async def analyze_resume_text(
    resume_text: str,
    role: str = "SDE"
):
    """
    Analyze resume text directly (for already parsed resumes).
    """
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    ats_result = calculate_ats_score(resume_text, role)
    
    return {
        "role": role,
        "ats_score": ats_result["ats_score"],
        "missing_skills": ats_result["missing_skills"],
        "weak_areas": ats_result["weak_areas"],
        "suggestions": ats_result["suggestions"]
    }


@router.get("/roles")
async def get_available_roles():
    """Get list of supported roles."""
    return {
        "roles": [
            {"id": "SDE", "name": "Software Development Engineer"},
            {"id": "Data Analyst", "name": "Data Analyst"},
            {"id": "ML Engineer", "name": "Machine Learning Engineer"}
        ]
    }


@router.post("/improve-bullet")
async def improve_bullet_point(request: BulletImproveRequest):
    """
    Improve a single resume bullet point.
    
    Takes a weak bullet point and transforms it into a strong,
    impactful statement with action verbs and metrics.
    """
    if not request.bullet or len(request.bullet.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Bullet point is too short"
        )
    
    result = improve_bullet(request.bullet, request.role)
    return result


@router.post("/improve-bullets-batch")
async def improve_bullets_batch(request: BatchBulletRequest):
    """
    Improve multiple resume bullet points at once.
    """
    if not request.bullets or len(request.bullets) == 0:
        raise HTTPException(
            status_code=400,
            detail="No bullet points provided"
        )
    
    results = batch_improve_bullets(request.bullets, request.role)
    return {"results": results}


@router.post("/career-recommendation")
async def get_career_recommendation(request: CareerAnalysisRequest):
    """
    Analyze resume and recommend best-fit career paths.
    
    Returns personalized career recommendations based on:
    - Technical skills detected
    - Experience patterns
    - Project types mentioned
    """
    if not request.resume_text or len(request.resume_text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Resume text is too short for analysis"
        )
    
    result = analyze_career_fit(request.resume_text, request.skills)
    return result


@router.get("/career-paths")
async def list_career_paths():
    """Get all available career paths for exploration."""
    return {"career_paths": get_all_career_paths()}


@router.get("/career-paths/{career_id}")
async def get_career_path(career_id: str):
    """Get detailed information about a specific career path."""
    details = get_career_path_details(career_id)
    if not details:
        raise HTTPException(
            status_code=404,
            detail="Career path not found"
        )
    return details
