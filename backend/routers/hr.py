from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random

from services.hr_analyzer import analyze_hr_response, get_hr_question_bank

router = APIRouter()


# Request models
class HRAnswerRequest(BaseModel):
    question: str
    answer: str


class StartHRRequest(BaseModel):
    pass


# In-memory session storage
hr_sessions = {}


@router.post("/hr-round")
async def evaluate_hr_answer(request: HRAnswerRequest):
    """
    Evaluate HR behavioral answer with strict validation.
    
    - Detects gibberish/random/invalid answers
    - Checks answer relevance to the question
    - Analyzes STAR method structure
    - Checks clarity and confidence
    - Returns realistic feedback like big tech interviews
    """
    if not request.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    if len(request.answer.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Answer is too short. Please provide a detailed response."
        )
    
    # Analyze the response with question context for relevance checking
    analysis = analyze_hr_response(request.answer, question=request.question)
    
    return {
        "question": request.question,
        "is_valid": analysis.get("is_valid", True),
        "scores": {
            "clarity": analysis["clarity"],
            "confidence": analysis["confidence"],
            "structure": analysis["structure"],
            "total": analysis["total_score"]
        },
        "feedback": analysis["feedback"],
        "details": analysis["details"],
        "red_flags": analysis["details"].get("red_flags", [])
    }


@router.post("/start")
async def start_hr_interview():
    """
    Start HR interview session with first question.
    """
    questions = get_hr_question_bank()
    first_question = random.choice(questions)
    
    import uuid
    session_id = str(uuid.uuid4())[:8]
    
    hr_sessions[session_id] = {
        "questions_asked": [first_question],
        "answers": [],
        "scores": [],
        "current_question": first_question
    }
    
    return {
        "session_id": session_id,
        "question": first_question["question"],
        "focus_areas": first_question["focus"],
        "question_number": 1,
        "message": "HR Interview started. Answer using the STAR method."
    }


@router.post("/submit/{session_id}")
async def submit_hr_answer(session_id: str, answer: str):
    """
    Submit HR answer for a session and get next question.
    """
    if session_id not in hr_sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Start a new HR interview."
        )
    
    if not answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    session = hr_sessions[session_id]
    current_q = session["current_question"]
    
    # Analyze response with question context for relevance checking
    analysis = analyze_hr_response(answer, question=current_q["question"])
    
    # Store results
    session["answers"].append({
        "question": current_q["question"],
        "answer": answer,
        "analysis": analysis
    })
    session["scores"].append(analysis["total_score"])
    
    # Get next question (avoid repeats)
    all_questions = get_hr_question_bank()
    asked_questions = [q["question"] for q in session["questions_asked"]]
    available = [q for q in all_questions if q["question"] not in asked_questions]
    
    if available:
        next_question = random.choice(available)
        session["questions_asked"].append(next_question)
        session["current_question"] = next_question
        has_next = True
    else:
        next_question = None
        has_next = False
    
    avg_score = sum(session["scores"]) // len(session["scores"])
    
    response = {
        "session_id": session_id,
        "evaluation": {
            "clarity": analysis["clarity"],
            "confidence": analysis["confidence"],
            "structure": analysis["structure"],
            "total": analysis["total_score"],
            "feedback": analysis["feedback"]
        },
        "session_stats": {
            "questions_answered": len(session["answers"]),
            "average_score": avg_score
        },
        "has_next_question": has_next
    }
    
    if has_next:
        response["next_question"] = {
            "question": next_question["question"],
            "focus_areas": next_question["focus"],
            "question_number": len(session["questions_asked"])
        }
    
    return response


@router.post("/end/{session_id}")
async def end_hr_session(session_id: str):
    """End HR session and get final summary."""
    if session_id not in hr_sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    session = hr_sessions[session_id]
    
    if not session["scores"]:
        del hr_sessions[session_id]
        return {"message": "Session ended with no answers", "score": 0}
    
    avg_score = sum(session["scores"]) // len(session["scores"])
    
    # Calculate average per category
    clarity_avg = sum(a["analysis"]["clarity"] for a in session["answers"]) // len(session["answers"])
    confidence_avg = sum(a["analysis"]["confidence"] for a in session["answers"]) // len(session["answers"])
    structure_avg = sum(a["analysis"]["structure"] for a in session["answers"]) // len(session["answers"])
    
    # Determine performance
    if avg_score >= 8:
        performance = "Excellent"
    elif avg_score >= 6:
        performance = "Good"
    elif avg_score >= 4:
        performance = "Average"
    else:
        performance = "Needs Improvement"
    
    summary = {
        "session_id": session_id,
        "total_questions": len(session["answers"]),
        "average_score": avg_score,
        "category_scores": {
            "clarity": clarity_avg,
            "confidence": confidence_avg,
            "structure": structure_avg
        },
        "performance": performance,
        "history": session["answers"]
    }
    
    del hr_sessions[session_id]
    
    return summary


@router.get("/questions")
async def get_hr_questions():
    """Get list of HR behavioral questions."""
    questions = get_hr_question_bank()
    return {
        "total": len(questions),
        "questions": questions
    }
