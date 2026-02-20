from typing import Dict, List
from config.skill_sets import get_skills_for_role
from services.ats_scorer import skill_found_in_resume


def analyze_skill_gaps(resume_text: str, role: str) -> Dict:
    """
    Analyze skill gaps between resume and role requirements.
    
    Args:
        resume_text: Plain text extracted from resume
        role: Target role (SDE, Data Analyst, ML Engineer)
        
    Returns:
        Dictionary with skill gap analysis
    """
    skills = get_skills_for_role(role)
    core_skills = skills["core_skills"]
    advanced_skills = skills["advanced_skills"]
    
    resume_lower = resume_text.lower()
    
    # Analyze core skills
    matched_core = []
    missing_core = []
    for skill in core_skills:
        if skill_found_in_resume(skill, resume_lower):
            matched_core.append(skill)
        else:
            missing_core.append(skill)
    
    # Analyze advanced skills
    matched_advanced = []
    missing_advanced = []
    for skill in advanced_skills:
        if skill_found_in_resume(skill, resume_lower):
            matched_advanced.append(skill)
        else:
            missing_advanced.append(skill)
    
    # Calculate match percentages
    total_skills = len(core_skills) + len(advanced_skills)
    total_matched = len(matched_core) + len(matched_advanced)
    
    skill_match_percentage = int((total_matched / total_skills) * 100) if total_skills > 0 else 0
    core_match_percentage = int((len(matched_core) / len(core_skills)) * 100) if core_skills else 0
    advanced_match_percentage = int((len(matched_advanced) / len(advanced_skills)) * 100) if advanced_skills else 0
    
    # Generate priority improvement order
    priority_improvement_order = generate_priority_order(
        missing_core, 
        missing_advanced, 
        role
    )
    
    return {
        "skill_match_percentage": skill_match_percentage,
        "core_match_percentage": core_match_percentage,
        "advanced_match_percentage": advanced_match_percentage,
        "matched_core_skills": matched_core,
        "matched_advanced_skills": matched_advanced,
        "missing_core_skills": missing_core,
        "missing_advanced_skills": missing_advanced,
        "priority_improvement_order": priority_improvement_order,
        "total_skills_required": total_skills,
        "total_skills_matched": total_matched
    }


def generate_priority_order(
    missing_core: List[str], 
    missing_advanced: List[str],
    role: str
) -> List[Dict]:
    """
    Generate prioritized list of skills to learn.
    Core skills come first, ordered by importance for the role.
    """
    priority_list = []
    
    # Priority weights for different roles
    role_priorities = {
        "SDE": {
            "Data Structures": 10,
            "Algorithms": 10,
            "Object-Oriented Programming": 9,
            "Problem Solving": 9,
            "Version Control (Git)": 8,
            "SQL": 7,
            "REST APIs": 7,
            "System Design": 8,
            "Docker & Kubernetes": 6,
        },
        "Data Analyst": {
            "SQL": 10,
            "Excel": 9,
            "Python/R": 9,
            "Data Visualization": 8,
            "Statistical Analysis": 8,
            "Tableau/Power BI": 7,
            "Data Cleaning": 7,
        },
        "ML Engineer": {
            "Python": 10,
            "Machine Learning Algorithms": 10,
            "Linear Algebra & Statistics": 9,
            "Scikit-learn": 8,
            "Deep Learning (TensorFlow/PyTorch)": 8,
            "Data Preprocessing": 7,
            "Model Deployment": 7,
        }
    }
    
    priorities = role_priorities.get(role, {})
    
    # Add core skills with high priority
    for skill in missing_core:
        weight = priorities.get(skill, 5)
        priority_list.append({
            "skill": skill,
            "priority": "high",
            "weight": weight,
            "category": "core",
            "reason": "Essential for role"
        })
    
    # Add advanced skills with medium priority
    for skill in missing_advanced:
        weight = priorities.get(skill, 3)
        priority_list.append({
            "skill": skill,
            "priority": "medium",
            "weight": weight,
            "category": "advanced",
            "reason": "Enhances competitiveness"
        })
    
    # Sort by weight (highest first)
    priority_list.sort(key=lambda x: x["weight"], reverse=True)
    
    return priority_list


def get_skill_gap_summary(resume_text: str, role: str) -> Dict:
    """
    Get a concise summary of skill gaps.
    """
    analysis = analyze_skill_gaps(resume_text, role)
    
    readiness_level = "Not Ready"
    if analysis["skill_match_percentage"] >= 80:
        readiness_level = "Highly Ready"
    elif analysis["skill_match_percentage"] >= 60:
        readiness_level = "Moderately Ready"
    elif analysis["skill_match_percentage"] >= 40:
        readiness_level = "Needs Improvement"
    
    top_priorities = [
        item["skill"] for item in analysis["priority_improvement_order"][:5]
    ]
    
    return {
        "readiness_level": readiness_level,
        "match_percentage": analysis["skill_match_percentage"],
        "core_gaps": len(analysis["missing_core_skills"]),
        "advanced_gaps": len(analysis["missing_advanced_skills"]),
        "top_priorities": top_priorities
    }
