"""
AI Career Path Recommender

Analyzes resume content to recommend best-fit career paths based on:
- Technical skills present
- Experience patterns
- Project types
- Education background
- Industry keywords
"""

from typing import Dict, List, Tuple
from collections import Counter
import re


# Career path definitions with skill weights and indicators
CAREER_PATHS = {
    "backend_engineering": {
        "title": "Backend Engineering",
        "description": "Design and build server-side applications, APIs, and databases",
        "icon": "🔧",
        "skills": {
            "strong": ["python", "java", "golang", "go", "rust", "c++", "node.js", "nodejs", 
                       "django", "flask", "fastapi", "spring", "express", "sql", "postgresql", 
                       "mysql", "mongodb", "redis", "docker", "kubernetes", "microservices",
                       "api", "rest", "graphql", "grpc", "backend", "server"],
            "moderate": ["linux", "aws", "azure", "gcp", "ci/cd", "git", "testing", 
                        "kafka", "rabbitmq", "nginx", "authentication", "security"],
        },
        "experience_keywords": ["api development", "backend", "server-side", "database design",
                               "scalability", "microservices", "distributed systems"],
        "companies": ["Backend Developer", "Software Engineer", "Platform Engineer"],
    },
    "frontend_engineering": {
        "title": "Frontend Engineering",
        "description": "Build interactive user interfaces and web applications",
        "icon": "🎨",
        "skills": {
            "strong": ["javascript", "typescript", "react", "reactjs", "vue", "vuejs", 
                       "angular", "html", "css", "sass", "tailwind", "webpack", "vite",
                       "nextjs", "next.js", "gatsby", "redux", "frontend", "ui", "ux"],
            "moderate": ["figma", "responsive", "accessibility", "seo", "animation",
                        "performance", "testing", "jest", "cypress"],
        },
        "experience_keywords": ["user interface", "frontend", "web development", "responsive design",
                               "user experience", "component", "spa", "single page"],
        "companies": ["Frontend Developer", "UI Engineer", "Web Developer"],
    },
    "fullstack_engineering": {
        "title": "Full Stack Engineering",
        "description": "End-to-end development across frontend and backend",
        "icon": "🚀",
        "skills": {
            "strong": ["javascript", "typescript", "python", "react", "node.js", "nodejs",
                       "express", "django", "flask", "sql", "mongodb", "html", "css",
                       "fullstack", "full-stack", "full stack"],
            "moderate": ["docker", "aws", "git", "rest", "api", "testing", "agile"],
        },
        "experience_keywords": ["full stack", "fullstack", "end-to-end", "frontend and backend",
                               "web application", "product development"],
        "companies": ["Full Stack Developer", "Software Engineer", "Product Engineer"],
    },
    "data_science": {
        "title": "Data Science",
        "description": "Extract insights from data using statistics and visualization",
        "icon": "📊",
        "skills": {
            "strong": ["python", "r", "sql", "pandas", "numpy", "matplotlib", "seaborn",
                       "tableau", "power bi", "statistics", "data analysis", "excel",
                       "jupyter", "data visualization", "analytics", "data science"],
            "moderate": ["hypothesis testing", "a/b testing", "regression", "correlation",
                        "dashboards", "reporting", "business intelligence", "bi"],
        },
        "experience_keywords": ["data analysis", "insights", "visualization", "reporting",
                               "business intelligence", "analytics", "metrics", "kpi"],
        "companies": ["Data Scientist", "Data Analyst", "Business Analyst"],
    },
    "machine_learning": {
        "title": "Machine Learning Engineering",
        "description": "Build and deploy ML models at scale",
        "icon": "🤖",
        "skills": {
            "strong": ["python", "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
                       "machine learning", "ml", "deep learning", "neural networks", "nlp",
                       "computer vision", "cv", "transformers", "huggingface", "llm"],
            "moderate": ["pandas", "numpy", "feature engineering", "model deployment",
                        "mlops", "docker", "aws sagemaker", "kubeflow", "mlflow"],
        },
        "experience_keywords": ["machine learning", "ml model", "training", "inference",
                               "deep learning", "neural network", "prediction", "classification"],
        "companies": ["ML Engineer", "AI Engineer", "Research Engineer"],
    },
    "data_engineering": {
        "title": "Data Engineering",
        "description": "Build data pipelines and infrastructure",
        "icon": "🔄",
        "skills": {
            "strong": ["python", "sql", "spark", "pyspark", "airflow", "kafka", "etl",
                       "data pipeline", "hadoop", "hive", "snowflake", "databricks",
                       "bigquery", "redshift", "data warehouse", "data engineering"],
            "moderate": ["docker", "kubernetes", "aws", "gcp", "azure", "scala",
                        "streaming", "batch processing", "data lake"],
        },
        "experience_keywords": ["data pipeline", "etl", "data warehouse", "data infrastructure",
                               "batch processing", "streaming", "data ingestion"],
        "companies": ["Data Engineer", "Analytics Engineer", "Platform Engineer"],
    },
    "devops_sre": {
        "title": "DevOps / SRE",
        "description": "Build and maintain reliable infrastructure and CI/CD",
        "icon": "⚙️",
        "skills": {
            "strong": ["docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
                       "ci/cd", "aws", "azure", "gcp", "linux", "bash", "devops",
                       "sre", "prometheus", "grafana", "monitoring"],
            "moderate": ["python", "go", "yaml", "helm", "argocd", "cloudformation",
                        "security", "networking", "load balancing"],
        },
        "experience_keywords": ["infrastructure", "deployment", "automation", "reliability",
                               "monitoring", "incident", "on-call", "scalability"],
        "companies": ["DevOps Engineer", "SRE", "Platform Engineer", "Cloud Engineer"],
    },
    "mobile_development": {
        "title": "Mobile Development",
        "description": "Build native and cross-platform mobile applications",
        "icon": "📱",
        "skills": {
            "strong": ["swift", "kotlin", "java", "react native", "flutter", "ios",
                       "android", "mobile", "xcode", "android studio", "dart"],
            "moderate": ["firebase", "push notifications", "app store", "play store",
                        "mobile ui", "offline", "sqlite"],
        },
        "experience_keywords": ["mobile app", "ios app", "android app", "cross-platform",
                               "app development", "native app"],
        "companies": ["Mobile Developer", "iOS Developer", "Android Developer"],
    },
    "security_engineering": {
        "title": "Security Engineering",
        "description": "Protect systems and data from threats",
        "icon": "🔒",
        "skills": {
            "strong": ["security", "cybersecurity", "penetration testing", "vulnerability",
                       "encryption", "authentication", "oauth", "jwt", "ssl", "tls",
                       "siem", "firewall", "ids", "ips"],
            "moderate": ["python", "linux", "networking", "compliance", "gdpr", "soc2",
                        "threat modeling", "incident response"],
        },
        "experience_keywords": ["security audit", "vulnerability assessment", "threat",
                               "compliance", "penetration test", "security architecture"],
        "companies": ["Security Engineer", "InfoSec Engineer", "Application Security"],
    },
    "product_management": {
        "title": "Product Management",
        "description": "Define product strategy and work with cross-functional teams",
        "icon": "📋",
        "skills": {
            "strong": ["product management", "roadmap", "user research", "agile", "scrum",
                       "jira", "product strategy", "stakeholder", "requirements",
                       "user stories", "mvp", "product"],
            "moderate": ["sql", "analytics", "a/b testing", "metrics", "okr", "kpi",
                        "wireframes", "prototyping"],
        },
        "experience_keywords": ["product launch", "feature prioritization", "user feedback",
                               "cross-functional", "product roadmap", "go-to-market"],
        "companies": ["Product Manager", "Technical PM", "Associate Product Manager"],
    },
}


def analyze_career_fit(resume_text: str, current_skills: List[str] = None) -> Dict:
    """
    Analyze resume and recommend best-fit career paths.
    
    Args:
        resume_text: Full text content of the resume
        current_skills: List of already-extracted skills (optional)
        
    Returns:
        Career recommendations with scores and insights
    """
    if not resume_text:
        return {
            "primary_recommendation": None,
            "all_recommendations": [],
            "analysis": "No resume content to analyze",
        }
    
    text_lower = resume_text.lower()
    
    # Calculate scores for each career path
    career_scores = {}
    career_details = {}
    
    for career_id, career_config in CAREER_PATHS.items():
        score, details = _calculate_career_score(text_lower, career_config, current_skills)
        career_scores[career_id] = score
        career_details[career_id] = details
    
    # Sort by score
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Build recommendations
    recommendations = []
    for career_id, score in sorted_careers:
        if score > 0:
            config = CAREER_PATHS[career_id]
            details = career_details[career_id]
            
            recommendations.append({
                "career_id": career_id,
                "title": config["title"],
                "description": config["description"],
                "icon": config["icon"],
                "fit_score": min(100, int(score)),
                "matching_skills": details["matching_skills"][:8],
                "experience_matches": details["experience_matches"][:3],
                "potential_roles": config["companies"][:3],
                "fit_level": _get_fit_level(score),
            })
    
    # Determine primary recommendation
    primary = recommendations[0] if recommendations else None
    
    # Generate insights
    insights = _generate_insights(primary, recommendations, text_lower)
    
    # Identify skill gaps for top recommendation
    skill_gaps = []
    if primary:
        config = CAREER_PATHS[primary["career_id"]]
        all_strong_skills = set(config["skills"]["strong"])
        matching = set(s.lower() for s in primary["matching_skills"])
        gaps = all_strong_skills - matching
        skill_gaps = list(gaps)[:5]
    
    return {
        "primary_recommendation": primary,
        "all_recommendations": recommendations[:5],  # Top 5
        "insights": insights,
        "skill_gaps_for_primary": skill_gaps,
        "career_diversity_score": _calculate_diversity(recommendations),
        "summary": _generate_summary(primary, recommendations),
    }


def _calculate_career_score(text: str, career_config: Dict, known_skills: List[str] = None) -> Tuple[float, Dict]:
    """Calculate how well the resume matches a career path."""
    score = 0
    matching_skills = []
    experience_matches = []
    
    # Check strong skills (higher weight)
    for skill in career_config["skills"]["strong"]:
        if _skill_in_text(skill, text):
            score += 10
            matching_skills.append(skill)
        elif known_skills and any(skill.lower() in s.lower() for s in known_skills):
            score += 8
            matching_skills.append(skill)
    
    # Check moderate skills (lower weight)
    for skill in career_config["skills"]["moderate"]:
        if _skill_in_text(skill, text):
            score += 5
            if skill not in matching_skills:
                matching_skills.append(skill)
    
    # Check experience keywords
    for keyword in career_config["experience_keywords"]:
        if keyword.lower() in text:
            score += 7
            experience_matches.append(keyword)
    
    # Bonus for explicit role mentions
    for role in career_config["companies"]:
        if role.lower() in text:
            score += 15
    
    # Normalize score (0-100)
    max_possible = (len(career_config["skills"]["strong"]) * 10 + 
                   len(career_config["skills"]["moderate"]) * 5 +
                   len(career_config["experience_keywords"]) * 7 +
                   len(career_config["companies"]) * 15)
    
    normalized_score = (score / max_possible * 100) if max_possible > 0 else 0
    
    return normalized_score, {
        "raw_score": score,
        "matching_skills": matching_skills,
        "experience_matches": experience_matches,
    }


def _skill_in_text(skill: str, text: str) -> bool:
    """Check if skill is present in text with word boundaries."""
    # Handle multi-word skills
    pattern = r'\b' + re.escape(skill.lower()) + r'\b'
    return bool(re.search(pattern, text))


def _get_fit_level(score: float) -> str:
    """Get fit level label from score."""
    if score >= 70:
        return "Excellent Fit"
    elif score >= 50:
        return "Strong Fit"
    elif score >= 30:
        return "Good Fit"
    elif score >= 15:
        return "Moderate Fit"
    else:
        return "Developing"


def _generate_insights(primary: Dict, all_recs: List[Dict], text: str) -> List[str]:
    """Generate personalized insights based on analysis."""
    insights = []
    
    if not primary:
        insights.append("Your resume could benefit from more technical keywords and specific skills.")
        return insights
    
    # Primary path insight
    if primary["fit_score"] >= 70:
        insights.append(f"Your profile strongly aligns with {primary['title']}. Your experience and skills are well-suited for this path.")
    elif primary["fit_score"] >= 50:
        insights.append(f"You show solid potential for {primary['title']}. Consider deepening expertise in core skills.")
    else:
        insights.append(f"You have foundational skills for {primary['title']}. Focus on building more relevant experience.")
    
    # Comparison insight
    if len(all_recs) >= 2:
        second = all_recs[1]
        score_diff = primary["fit_score"] - second["fit_score"]
        if score_diff < 10:
            insights.append(f"You're equally suited for {primary['title']} and {second['title']}. Consider which path excites you more.")
        elif score_diff < 20:
            insights.append(f"{second['title']} is also a strong option for you, with transferable skills.")
    
    # Skill-based insights
    if len(primary["matching_skills"]) >= 6:
        insights.append("You have a diverse technical skill set that employers value.")
    
    # Career transition insight
    backend_keywords = ["api", "backend", "server", "database"]
    frontend_keywords = ["react", "ui", "frontend", "css", "javascript"]
    ml_keywords = ["machine learning", "ml", "neural", "tensorflow", "pytorch"]
    
    has_backend = any(k in text for k in backend_keywords)
    has_frontend = any(k in text for k in frontend_keywords)
    has_ml = any(k in text for k in ml_keywords)
    
    if has_backend and has_frontend:
        insights.append("Your combined frontend and backend skills position you well for Full Stack roles.")
    
    if has_ml and has_backend:
        insights.append("Your ML and engineering skills could be valuable for MLOps or AI Platform roles.")
    
    return insights[:4]


def _calculate_diversity(recommendations: List[Dict]) -> str:
    """Calculate how diverse the candidate's skills are across career paths."""
    if len(recommendations) < 2:
        return "Focused"
    
    scores_above_30 = sum(1 for r in recommendations if r["fit_score"] >= 30)
    
    if scores_above_30 >= 4:
        return "Highly Versatile"
    elif scores_above_30 >= 3:
        return "Versatile"
    elif scores_above_30 >= 2:
        return "Balanced"
    else:
        return "Specialized"


def _generate_summary(primary: Dict, all_recs: List[Dict]) -> str:
    """Generate a natural language summary."""
    if not primary:
        return "Upload a resume with more technical details for career recommendations."
    
    if primary["fit_score"] >= 60:
        return f"Your resume suggests strong alignment with {primary['title']} roles. Your {', '.join(primary['matching_skills'][:3])} skills are particularly relevant."
    elif primary["fit_score"] >= 40:
        return f"You are well-suited for {primary['title']} positions. Building experience in {primary['title'].lower()} would strengthen your profile."
    else:
        second_mention = f" or {all_recs[1]['title']}" if len(all_recs) > 1 else ""
        return f"Consider focusing on {primary['title']}{second_mention} based on your current skills. Adding more relevant projects would help."


def get_career_path_details(career_id: str) -> Dict:
    """Get detailed information about a specific career path."""
    if career_id not in CAREER_PATHS:
        return None
    
    config = CAREER_PATHS[career_id]
    return {
        "career_id": career_id,
        "title": config["title"],
        "description": config["description"],
        "icon": config["icon"],
        "key_skills": config["skills"]["strong"][:10],
        "supporting_skills": config["skills"]["moderate"][:8],
        "typical_roles": config["companies"],
        "experience_areas": config["experience_keywords"][:5],
    }


def get_all_career_paths() -> List[Dict]:
    """Get summary of all available career paths."""
    return [
        {
            "career_id": cid,
            "title": config["title"],
            "icon": config["icon"],
            "description": config["description"],
        }
        for cid, config in CAREER_PATHS.items()
    ]
