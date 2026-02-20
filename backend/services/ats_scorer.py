import re
from typing import Dict, List
from config.skill_sets import get_skills_for_role


def calculate_ats_score(resume_text: str, role: str) -> Dict:
    """
    Calculate ATS score by comparing resume against role requirements.
    
    Args:
        resume_text: Plain text extracted from resume
        role: Target role (SDE, Data Analyst, ML Engineer)
        
    Returns:
        Dictionary with ATS analysis results
    """
    skills = get_skills_for_role(role)
    core_skills = skills["core_skills"]
    advanced_skills = skills["advanced_skills"]
    
    # Normalize resume text for matching
    resume_lower = resume_text.lower()
    
    # Find matched and missing skills
    matched_core = []
    missing_core = []
    matched_advanced = []
    missing_advanced = []
    weak_areas = []
    
    for skill in core_skills:
        if skill_found_in_resume(skill, resume_lower):
            matched_core.append(skill)
        else:
            missing_core.append(skill)
    
    for skill in advanced_skills:
        if skill_found_in_resume(skill, resume_lower):
            matched_advanced.append(skill)
        else:
            missing_advanced.append(skill)
    
    # Calculate scores
    total_skills = len(core_skills) + len(advanced_skills)
    matched_skills = len(matched_core) + len(matched_advanced)
    
    # Core skills weighted more heavily (60% core, 40% advanced)
    core_score = (len(matched_core) / len(core_skills)) * 60 if core_skills else 0
    advanced_score = (len(matched_advanced) / len(advanced_skills)) * 40 if advanced_skills else 0
    
    ats_score = int(core_score + advanced_score)
    
    # Identify weak areas (core skills that are missing)
    weak_areas = missing_core[:3]  # Top 3 missing core skills are weak areas
    
    # Combine all missing skills
    missing_skills = missing_core + missing_advanced
    
    # Generate suggestions
    suggestions = generate_suggestions(missing_core, missing_advanced, ats_score)
    
    return {
        "ats_score": ats_score,
        "missing_skills": missing_skills,
        "weak_areas": weak_areas,
        "suggestions": suggestions,
        "matched_skills": matched_core + matched_advanced,
        "core_match": f"{len(matched_core)}/{len(core_skills)}",
        "advanced_match": f"{len(matched_advanced)}/{len(advanced_skills)}"
    }


def skill_found_in_resume(skill: str, resume_lower: str) -> bool:
    """
    Check if a skill is mentioned in the resume.
    Handles variations and common abbreviations.
    """
    skill_lower = skill.lower()
    
    # Direct match
    if skill_lower in resume_lower:
        return True
    
    # Handle skill variations
    skill_variations = get_skill_variations(skill)
    for variation in skill_variations:
        if variation.lower() in resume_lower:
            return True
    
    # Word boundary match for short skills
    pattern = r'\b' + re.escape(skill_lower) + r'\b'
    if re.search(pattern, resume_lower):
        return True
    
    return False


def get_skill_variations(skill: str) -> List[str]:
    """Get common variations of a skill name."""
    variations = {
        "Data Structures": ["data structure", "ds", "dsa"],
        "Algorithms": ["algorithm", "algo"],
        "Object-Oriented Programming": ["oop", "object oriented", "oops"],
        "Version Control (Git)": ["git", "github", "gitlab", "version control"],
        "SQL": ["mysql", "postgresql", "postgres", "sqlite", "sql server"],
        "REST APIs": ["rest", "restful", "api", "apis"],
        "Testing & Debugging": ["testing", "debugging", "unit test", "pytest", "jest"],
        "System Design": ["system design", "architecture", "hld", "lld"],
        "Microservices Architecture": ["microservices", "micro-services", "microservice"],
        "Cloud Services (AWS/GCP/Azure)": ["aws", "gcp", "azure", "cloud", "ec2", "s3"],
        "CI/CD Pipelines": ["ci/cd", "cicd", "jenkins", "github actions", "gitlab ci"],
        "Docker & Kubernetes": ["docker", "kubernetes", "k8s", "container"],
        "Python/R": ["python", "r programming", "r language"],
        "Data Visualization": ["visualization", "charts", "graphs", "matplotlib", "seaborn"],
        "Excel": ["excel", "spreadsheet", "xlsx"],
        "Tableau/Power BI": ["tableau", "power bi", "powerbi"],
        "Machine Learning Algorithms": ["machine learning", "ml", "supervised", "unsupervised"],
        "Deep Learning (TensorFlow/PyTorch)": ["tensorflow", "pytorch", "keras", "deep learning", "neural network"],
        "NumPy & Pandas": ["numpy", "pandas", "np", "pd"],
        "Scikit-learn": ["sklearn", "scikit", "scikit-learn"],
        "NLP/Computer Vision": ["nlp", "natural language", "computer vision", "cv", "opencv"],
        "MLOps": ["mlops", "ml ops", "mlflow", "kubeflow"],
    }
    
    return variations.get(skill, [])


def generate_suggestions(missing_core: List[str], missing_advanced: List[str], score: int) -> List[str]:
    """Generate improvement suggestions based on analysis."""
    suggestions = []
    
    if score < 40:
        suggestions.append("Your resume needs significant improvements to match this role")
    elif score < 60:
        suggestions.append("Focus on adding more relevant skills to improve your match")
    elif score < 80:
        suggestions.append("Good foundation! Consider highlighting advanced skills")
    else:
        suggestions.append("Excellent match! Fine-tune with industry keywords")
    
    if missing_core:
        suggestions.append(f"Add these core skills: {', '.join(missing_core[:3])}")
    
    if missing_advanced and score >= 60:
        suggestions.append(f"Consider learning: {', '.join(missing_advanced[:2])}")
    
    suggestions.append("Use action verbs and quantify achievements where possible")
    
    return suggestions
