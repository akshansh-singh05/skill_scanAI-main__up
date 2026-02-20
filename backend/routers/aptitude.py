"""
Router for Aptitude & Situational Interview Questions
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from services.aptitude_questions import (
    get_aptitude_questions,
    get_situational_questions,
    get_case_studies,
    check_aptitude_answer,
    check_situational_answer,
    get_random_aptitude_quiz,
    get_random_situational_quiz,
)

router = APIRouter(prefix="/aptitude", tags=["aptitude"])


class AptitudeAnswerRequest(BaseModel):
    question_id: str
    answer: str


class QuizRequest(BaseModel):
    count: int = 10
    categories: Optional[List[str]] = None


# ============ Aptitude Questions ============

@router.get("/questions")
async def list_aptitude_questions(
    category: Optional[str] = Query(None, description="Filter by category: Quantitative, Logical Reasoning, Data Interpretation"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: Easy, Medium, Hard")
):
    """Get all aptitude questions with optional filters."""
    questions = get_aptitude_questions(category=category, difficulty=difficulty)
    
    # Return questions without answers for practice
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q["id"],
            "title": q["title"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"],
            "topic": q.get("topic", "General")
        })
    
    return {"questions": sanitized, "total": len(sanitized)}


@router.post("/check-answer")
async def check_answer(request: AptitudeAnswerRequest):
    """Check if the answer to an aptitude question is correct."""
    result = check_aptitude_answer(request.question_id, request.answer)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/quiz")
async def get_quiz(
    count: int = Query(10, ge=1, le=20, description="Number of questions"),
    categories: Optional[str] = Query(None, description="Comma-separated categories")
):
    """Get a random aptitude quiz."""
    cat_list = None
    if categories:
        cat_list = [c.strip() for c in categories.split(",")]
    
    questions = get_random_aptitude_quiz(count=count, categories=cat_list)
    
    # Sanitize questions (remove answers)
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q["id"],
            "title": q["title"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"],
            "topic": q.get("topic", "General")
        })
    
    return {"questions": sanitized, "total": len(sanitized)}


# ============ Situational Judgment Questions ============

@router.get("/situational")
async def list_situational_questions(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: Easy, Medium, Hard")
):
    """Get all situational judgment questions."""
    questions = get_situational_questions(difficulty=difficulty)
    
    # Return questions without answers
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q["id"],
            "title": q["title"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "scenario": q["scenario"],
            "question": q["question"],
            "options": q["options"],
            "competencies": q["competencies"]
        })
    
    return {"questions": sanitized, "total": len(sanitized)}


@router.post("/situational/check-answer")
async def check_situational(request: AptitudeAnswerRequest):
    """Check situational judgment answer and get feedback."""
    result = check_situational_answer(request.question_id, request.answer)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/situational/quiz")
async def get_situational_quiz(
    count: int = Query(5, ge=1, le=10, description="Number of questions")
):
    """Get a random situational judgment quiz."""
    questions = get_random_situational_quiz(count=count)
    
    # Sanitize questions
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q["id"],
            "title": q["title"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "scenario": q["scenario"],
            "question": q["question"],
            "options": q["options"],
            "competencies": q["competencies"]
        })
    
    return {"questions": sanitized, "total": len(sanitized)}


# ============ Case Studies ============

@router.get("/case-studies")
async def list_case_studies():
    """Get all case study questions for in-depth practice."""
    case_studies = get_case_studies()
    return {"case_studies": case_studies, "total": len(case_studies)}


@router.get("/case-studies/{case_id}")
async def get_case_study(case_id: str):
    """Get a specific case study by ID."""
    case_studies = get_case_studies()
    
    for case in case_studies:
        if case["id"] == case_id:
            return case
    
    raise HTTPException(status_code=404, detail="Case study not found")


# ============ Categories Overview ============

@router.get("/categories")
async def get_categories():
    """Get overview of all question categories available."""
    return {
        "categories": [
            {
                "id": "quantitative",
                "name": "Quantitative Aptitude",
                "description": "Mathematical and numerical problems",
                "topics": ["Profit & Loss", "Time & Work", "Speed & Distance", "Percentages", "Ratio & Proportion", "Interest", "Averages"]
            },
            {
                "id": "logical",
                "name": "Logical Reasoning",
                "description": "Pattern recognition and logical problems",
                "topics": ["Number Series", "Letter Series", "Blood Relations", "Direction Sense", "Coding-Decoding", "Syllogism", "Clocks", "Seating Arrangement"]
            },
            {
                "id": "data_interpretation",
                "name": "Data Interpretation",
                "description": "Analyze charts, graphs, and data tables",
                "topics": ["Bar Graphs", "Pie Charts", "Line Graphs", "Tables"]
            },
            {
                "id": "situational",
                "name": "Situational Judgment",
                "description": "Workplace scenarios and behavioral questions",
                "topics": ["Conflict Resolution", "Leadership", "Communication", "Ethics", "Time Management", "Team Work"]
            },
            {
                "id": "case_study",
                "name": "Case Studies",
                "description": "In-depth analysis and decision-making scenarios",
                "topics": ["System Design", "Crisis Management", "Team Building", "Product Decisions"]
            }
        ]
    }
