from typing import Dict, List, Optional


# Weight configuration for different score components
SCORE_WEIGHTS = {
    "resume": 0.30,      # 30% weight
    "technical": 0.45,   # 45% weight
    "hr": 0.25           # 25% weight
}

# Readiness level thresholds
READINESS_LEVELS = {
    "highly_ready": {"min": 80, "label": "Highly Ready", "color": "green"},
    "ready": {"min": 65, "label": "Ready", "color": "blue"},
    "moderately_ready": {"min": 50, "label": "Moderately Ready", "color": "yellow"},
    "needs_improvement": {"min": 35, "label": "Needs Improvement", "color": "orange"},
    "not_ready": {"min": 0, "label": "Not Ready", "color": "red"}
}


def generate_final_report(
    resume_score: int,
    technical_score: int,
    hr_score: int,
    resume_details: Optional[Dict] = None,
    technical_details: Optional[Dict] = None,
    hr_details: Optional[Dict] = None,
    role: str = "SDE"
) -> Dict:
    """
    Generate comprehensive final assessment report.
    
    Args:
        resume_score: ATS/resume analysis score (0-100)
        technical_score: Technical interview score (0-100)
        hr_score: HR behavioral interview score (0-100)
        resume_details: Optional detailed resume analysis
        technical_details: Optional detailed technical analysis
        hr_details: Optional detailed HR analysis
        role: Target role
        
    Returns:
        Complete assessment report
    """
    # Calculate weighted average
    weighted_score = calculate_weighted_average(resume_score, technical_score, hr_score)
    
    # Determine readiness level
    readiness = determine_readiness_level(weighted_score)
    
    # Generate improvement checklist
    improvement_checklist = generate_improvement_checklist(
        resume_score, technical_score, hr_score,
        resume_details, technical_details, hr_details
    )
    
    # Generate strengths and weaknesses
    strengths, weaknesses = identify_strengths_weaknesses(
        resume_score, technical_score, hr_score
    )
    
    # Generate action items
    action_items = generate_action_items(
        resume_score, technical_score, hr_score, role
    )
    
    return {
        "overall_readiness": weighted_score,
        "readiness_level": readiness["label"],
        "readiness_color": readiness["color"],
        "scores": {
            "resume_score": resume_score,
            "technical_score": technical_score,
            "hr_score": hr_score,
            "weighted_average": weighted_score
        },
        "weights": SCORE_WEIGHTS,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvement_checklist": improvement_checklist,
        "action_items": action_items,
        "role": role,
        "summary": generate_summary(weighted_score, readiness["label"], role)
    }


def calculate_weighted_average(
    resume_score: int,
    technical_score: int,
    hr_score: int
) -> int:
    """Calculate weighted average of all scores."""
    weighted = (
        resume_score * SCORE_WEIGHTS["resume"] +
        technical_score * SCORE_WEIGHTS["technical"] +
        hr_score * SCORE_WEIGHTS["hr"]
    )
    return int(weighted)


def determine_readiness_level(score: int) -> Dict:
    """Determine readiness level based on overall score."""
    for level_key in ["highly_ready", "ready", "moderately_ready", "needs_improvement", "not_ready"]:
        level = READINESS_LEVELS[level_key]
        if score >= level["min"]:
            return level
    return READINESS_LEVELS["not_ready"]


def generate_improvement_checklist(
    resume_score: int,
    technical_score: int,
    hr_score: int,
    resume_details: Optional[Dict] = None,
    technical_details: Optional[Dict] = None,
    hr_details: Optional[Dict] = None
) -> List[Dict]:
    """Generate prioritized improvement checklist."""
    checklist = []
    
    # Resume improvements
    if resume_score < 80:
        checklist.append({
            "category": "Resume",
            "priority": "high" if resume_score < 50 else "medium",
            "items": get_resume_improvements(resume_score, resume_details)
        })
    
    # Technical improvements
    if technical_score < 80:
        checklist.append({
            "category": "Technical Skills",
            "priority": "high" if technical_score < 50 else "medium",
            "items": get_technical_improvements(technical_score, technical_details)
        })
    
    # HR improvements
    if hr_score < 80:
        checklist.append({
            "category": "Behavioral/HR",
            "priority": "high" if hr_score < 50 else "medium",
            "items": get_hr_improvements(hr_score, hr_details)
        })
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    checklist.sort(key=lambda x: priority_order.get(x["priority"], 2))
    
    return checklist


def get_resume_improvements(score: int, details: Optional[Dict] = None) -> List[str]:
    """Get resume-specific improvement items."""
    items = []
    
    if score < 40:
        items.append("Significantly revise resume to include relevant skills and keywords")
        items.append("Add quantifiable achievements and metrics")
        items.append("Ensure proper formatting for ATS compatibility")
    elif score < 60:
        items.append("Add more industry-specific keywords")
        items.append("Highlight relevant projects and experience")
        items.append("Include measurable outcomes in experience descriptions")
    elif score < 80:
        items.append("Fine-tune keyword optimization")
        items.append("Add any missing technical skills")
    
    if details and details.get("missing_skills"):
        missing = details["missing_skills"][:3]
        items.append(f"Add missing skills: {', '.join(missing)}")
    
    return items


def get_technical_improvements(score: int, details: Optional[Dict] = None) -> List[str]:
    """Get technical skills improvement items."""
    items = []
    
    if score < 40:
        items.append("Review fundamental data structures and algorithms")
        items.append("Practice coding problems daily on LeetCode/HackerRank")
        items.append("Study core concepts for your target role")
    elif score < 60:
        items.append("Practice medium-difficulty coding problems")
        items.append("Work on explaining your thought process clearly")
        items.append("Review system design basics")
    elif score < 80:
        items.append("Focus on edge cases and optimization")
        items.append("Practice harder problems")
        items.append("Improve communication during problem-solving")
    
    if details and details.get("weak_areas"):
        weak = details["weak_areas"][:2]
        items.append(f"Focus on weak areas: {', '.join(weak)}")
    
    return items


def get_hr_improvements(score: int, details: Optional[Dict] = None) -> List[str]:
    """Get HR/behavioral improvement items."""
    items = []
    
    if score < 40:
        items.append("Learn and practice the STAR method")
        items.append("Prepare 5-7 stories covering different competencies")
        items.append("Practice speaking with confidence and clarity")
    elif score < 60:
        items.append("Add more specific details and metrics to your stories")
        items.append("Practice articulating your impact clearly")
        items.append("Work on showing leadership and ownership")
    elif score < 80:
        items.append("Refine your stories with stronger outcomes")
        items.append("Practice handling follow-up questions")
    
    if details:
        if details.get("structure", 0) < 6:
            items.append("Structure answers using STAR: Situation, Task, Action, Result")
        if details.get("confidence", 0) < 6:
            items.append("Use more action verbs and avoid hedging language")
        if details.get("clarity", 0) < 6:
            items.append("Keep answers concise (2-3 minutes per response)")
    
    return items


def identify_strengths_weaknesses(
    resume_score: int,
    technical_score: int,
    hr_score: int
) -> tuple:
    """Identify key strengths and weaknesses."""
    categories = [
        ("Resume/ATS", resume_score),
        ("Technical Skills", technical_score),
        ("Behavioral/HR", hr_score)
    ]
    
    # Sort by score
    sorted_categories = sorted(categories, key=lambda x: x[1], reverse=True)
    
    strengths = []
    weaknesses = []
    
    for category, score in sorted_categories:
        if score >= 70:
            strengths.append({
                "area": category,
                "score": score,
                "label": "Strong" if score >= 80 else "Good"
            })
        elif score < 50:
            weaknesses.append({
                "area": category,
                "score": score,
                "label": "Needs Work" if score >= 35 else "Critical"
            })
    
    return strengths, weaknesses


def generate_action_items(
    resume_score: int,
    technical_score: int,
    hr_score: int,
    role: str
) -> List[Dict]:
    """Generate specific action items with timeframes."""
    actions = []
    
    # Determine lowest score area
    scores = {
        "resume": resume_score,
        "technical": technical_score,
        "hr": hr_score
    }
    
    min_area = min(scores, key=scores.get)
    min_score = scores[min_area]
    
    # Immediate actions (this week)
    if min_score < 50:
        if min_area == "resume":
            actions.append({
                "action": "Revise resume with role-specific keywords",
                "timeframe": "This Week",
                "priority": "critical"
            })
        elif min_area == "technical":
            actions.append({
                "action": "Start daily coding practice (30 min minimum)",
                "timeframe": "This Week",
                "priority": "critical"
            })
        else:
            actions.append({
                "action": "Prepare 3 STAR stories for common HR questions",
                "timeframe": "This Week",
                "priority": "critical"
            })
    
    # Short-term actions (2 weeks)
    actions.append({
        "action": f"Complete 10 practice problems for {role} interviews",
        "timeframe": "2 Weeks",
        "priority": "high"
    })
    
    if hr_score < 70:
        actions.append({
            "action": "Record yourself answering HR questions and review",
            "timeframe": "2 Weeks",
            "priority": "medium"
        })
    
    # Medium-term actions (1 month)
    if technical_score < 70:
        actions.append({
            "action": "Complete a system design or advanced topic course",
            "timeframe": "1 Month",
            "priority": "medium"
        })
    
    actions.append({
        "action": "Do 2-3 mock interviews with peers or mentors",
        "timeframe": "1 Month",
        "priority": "high"
    })
    
    return actions


def generate_summary(overall_score: int, readiness_level: str, role: str) -> str:
    """Generate human-readable summary."""
    if overall_score >= 80:
        return f"Excellent preparation for {role} roles! You demonstrate strong skills across all areas. Focus on maintaining your edge and practicing under real interview conditions."
    elif overall_score >= 65:
        return f"Good preparation for {role} interviews. You have a solid foundation with some areas to strengthen. Follow the improvement checklist to boost your readiness."
    elif overall_score >= 50:
        return f"Moderate preparation for {role} roles. You have potential but need focused improvement in key areas. Prioritize the high-priority items in your checklist."
    elif overall_score >= 35:
        return f"Your {role} interview preparation needs significant work. Focus on fundamentals and practice consistently. Consider dedicating 2-4 weeks of focused preparation."
    else:
        return f"Substantial preparation needed for {role} interviews. Start with the basics and build up systematically. Consider a structured preparation program."


def get_score_breakdown_chart_data(
    resume_score: int,
    technical_score: int,
    hr_score: int
) -> Dict:
    """Get data formatted for chart visualization."""
    return {
        "labels": ["Resume/ATS", "Technical", "HR/Behavioral"],
        "scores": [resume_score, technical_score, hr_score],
        "weights": [
            SCORE_WEIGHTS["resume"] * 100,
            SCORE_WEIGHTS["technical"] * 100,
            SCORE_WEIGHTS["hr"] * 100
        ],
        "colors": [
            get_score_color(resume_score),
            get_score_color(technical_score),
            get_score_color(hr_score)
        ]
    }


def get_score_color(score: int) -> str:
    """Get color code based on score."""
    if score >= 80:
        return "#22c55e"  # green
    elif score >= 65:
        return "#3b82f6"  # blue
    elif score >= 50:
        return "#eab308"  # yellow
    elif score >= 35:
        return "#f97316"  # orange
    else:
        return "#ef4444"  # red
