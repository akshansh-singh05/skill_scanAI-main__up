from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.interview_engine import generate_question, evaluate_answer, generate_company_question
from config.company_modes import get_company_config, get_all_companies, get_interview_strategy, get_company_questions
from services.communication_analyzer import analyze_communication, get_communication_grade

router = APIRouter()


# Request/Response models
class StartInterviewRequest(BaseModel):
    role: str = "SDE"
    difficulty: str = "medium"
    company: str = "generic"


class SubmitAnswerRequest(BaseModel):
    question: str
    answer: str
    difficulty: str
    role: str
    company: str = "generic"
    question_type: str = "technical"


class AnalyzeCommunicationRequest(BaseModel):
    text: str
    is_behavioral: bool = False


class InterviewState(BaseModel):
    role: str
    current_question: str
    current_difficulty: str
    questions_asked: int
    total_score: int
    history: List[dict]


# In-memory session storage (for hackathon demo)
sessions = {}


@router.get("/companies")
async def get_companies():
    """Get all available company interview modes."""
    return {"companies": get_all_companies()}


@router.get("/company/{company_id}")
async def get_company_details(company_id: str):
    """Get detailed interview strategy for a specific company."""
    config = get_company_config(company_id)
    if config["name"] == "General Practice" and company_id != "generic":
        raise HTTPException(status_code=404, detail="Company not found")
    
    strategy = get_interview_strategy(company_id)
    return strategy


@router.post("/start-interview")
async def start_interview(request: StartInterviewRequest):
    """
    Start a new technical interview session.
    
    - Generates first question based on role, difficulty, and company
    - Returns session ID and first question
    """
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    valid_difficulties = ["easy", "medium", "hard"]
    if request.difficulty.lower() not in valid_difficulties:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty. Choose from: {', '.join(valid_difficulties)}"
        )
    
    # Get company config
    company_config = get_company_config(request.company)
    
    # Generate first question with company context
    question_data = generate_company_question(
        role=request.role,
        difficulty=request.difficulty,
        company=request.company
    )
    
    # Create session
    import uuid
    session_id = str(uuid.uuid4())[:8]
    
    sessions[session_id] = {
        "role": request.role,
        "company": request.company,
        "current_difficulty": request.difficulty,
        "questions_asked": 1,
        "total_score": 0,
        "history": [],
        "current_question": question_data
    }
    
    return {
        "session_id": session_id,
        "role": request.role,
        "company": company_config["name"],
        "company_style": company_config["style"],
        "question": question_data["question"],
        "difficulty": question_data["difficulty"],
        "question_type": question_data.get("question_type", "technical"),
        "question_number": 1,
        "tips": company_config.get("tips", [])[:2],
        "message": f"Interview started in {company_config['name']} mode. Answer the question below."
    }


@router.post("/analyze-communication")
async def analyze_communication_endpoint(request: AnalyzeCommunicationRequest):
    """
    Analyze text for communication quality.
    Returns scores for clarity, structure, and confidence.
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )
    
    analysis = analyze_communication(request.text, request.is_behavioral)
    
    return {
        "analysis": analysis,
        "grades": {
            "overall": get_communication_grade(analysis["overall_score"]),
            "clarity": get_communication_grade(analysis["clarity_score"]),
            "structure": get_communication_grade(analysis["structure_score"]),
            "confidence": get_communication_grade(analysis["confidence_score"]),
        }
    }


@router.post("/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit answer and get evaluation with next question.
    
    - Evaluates the submitted answer
    - Adjusts difficulty based on performance
    - Analyzes communication quality
    - Returns feedback and next question (company-specific)
    """
    if not request.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    # Determine if this is a behavioral question
    is_behavioral = request.question_type in ["behavioral", "leadership"]
    
    # Analyze communication quality
    comm_analysis = analyze_communication(request.answer, is_behavioral)
    
    # Evaluate answer
    evaluation = evaluate_answer(
        question=request.question,
        answer=request.answer,
        difficulty=request.difficulty,
        role=request.role
    )
    
    # Generate next question with adjusted difficulty and company context
    next_question_data = generate_company_question(
        role=request.role,
        difficulty=evaluation["next_difficulty"],
        company=request.company
    )
    
    # Get company config for additional context
    company_config = get_company_config(request.company)
    
    return {
        "evaluation": {
            "score": evaluation["evaluation_score"],
            "feedback": evaluation["feedback"],
            "breakdown": evaluation["breakdown"]
        },
        "communication": {
            "clarity_score": comm_analysis["clarity_score"],
            "structure_score": comm_analysis["structure_score"],
            "confidence_score": comm_analysis["confidence_score"],
            "overall_score": comm_analysis["overall_score"],
            "filler_words": comm_analysis["filler_words"][:3],
            "filler_count": comm_analysis["filler_count"],
            "issues": comm_analysis["issues"],
            "suggestions": comm_analysis["suggestions"],
            "strengths": comm_analysis["strengths"],
            "word_count": comm_analysis["word_count"],
            "grades": {
                "clarity": get_communication_grade(comm_analysis["clarity_score"]),
                "structure": get_communication_grade(comm_analysis["structure_score"]),
            }
        },
        "next_question": {
            "question": next_question_data["question"],
            "difficulty": next_question_data["difficulty"],
            "question_type": next_question_data.get("question_type", "technical"),
            "company": company_config["name"]
        },
        "difficulty_change": {
            "previous": request.difficulty,
            "next": evaluation["next_difficulty"]
        }
    }


@router.post("/submit-answer/{session_id}")
async def submit_answer_with_session(session_id: str, answer: str):
    """
    Submit answer for a specific session.
    Tracks history and cumulative scoring.
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Start a new interview."
        )
    
    session = sessions[session_id]
    current_q = session["current_question"]
    
    if not answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    # Evaluate answer
    evaluation = evaluate_answer(
        question=current_q["question"],
        answer=answer,
        difficulty=current_q["difficulty"],
        role=session["role"]
    )
    
    # Update session
    session["history"].append({
        "question": current_q["question"],
        "answer": answer,
        "score": evaluation["evaluation_score"],
        "difficulty": current_q["difficulty"]
    })
    session["total_score"] += evaluation["evaluation_score"]
    session["questions_asked"] += 1
    
    # Generate next question
    next_question_data = generate_question(
        session["role"],
        evaluation["next_difficulty"]
    )
    session["current_question"] = next_question_data
    session["current_difficulty"] = evaluation["next_difficulty"]
    
    # Calculate average score
    avg_score = session["total_score"] // len(session["history"])
    
    return {
        "session_id": session_id,
        "evaluation": {
            "score": evaluation["evaluation_score"],
            "feedback": evaluation["feedback"],
            "breakdown": evaluation["breakdown"]
        },
        "next_question": {
            "question": next_question_data["question"],
            "difficulty": next_question_data["difficulty"],
            "question_number": session["questions_asked"]
        },
        "session_stats": {
            "questions_answered": len(session["history"]),
            "average_score": avg_score,
            "current_difficulty": session["current_difficulty"]
        }
    }


@router.get("/session/{session_id}")
async def get_session_status(session_id: str):
    """Get current session status and history."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    session = sessions[session_id]
    avg_score = session["total_score"] // len(session["history"]) if session["history"] else 0
    
    return {
        "session_id": session_id,
        "role": session["role"],
        "current_difficulty": session["current_difficulty"],
        "questions_answered": len(session["history"]),
        "average_score": avg_score,
        "current_question": session["current_question"]["question"],
        "history": session["history"]
    }


@router.post("/end-session/{session_id}")
async def end_session(session_id: str):
    """End interview session and get final summary."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    session = sessions[session_id]
    
    if not session["history"]:
        # Clean up and return
        del sessions[session_id]
        return {"message": "Session ended with no answers submitted", "score": 0}
    
    avg_score = session["total_score"] // len(session["history"])
    
    # Determine performance level
    if avg_score >= 80:
        performance = "Excellent"
    elif avg_score >= 60:
        performance = "Good"
    elif avg_score >= 40:
        performance = "Average"
    else:
        performance = "Needs Improvement"
    
    summary = {
        "session_id": session_id,
        "role": session["role"],
        "total_questions": len(session["history"]),
        "average_score": avg_score,
        "performance": performance,
        "history": session["history"]
    }
    
    # Clean up session
    del sessions[session_id]
    
    return summary
