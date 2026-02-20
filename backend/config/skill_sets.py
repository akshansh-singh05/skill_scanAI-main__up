SKILL_SETS = {
    "SDE": {
        "core_skills": [
            "Data Structures",
            "Algorithms",
            "Object-Oriented Programming",
            "Version Control (Git)",
            "Problem Solving",
            "SQL",
            "REST APIs",
            "Testing & Debugging"
        ],
        "advanced_skills": [
            "System Design",
            "Microservices Architecture",
            "Cloud Services (AWS/GCP/Azure)",
            "CI/CD Pipelines",
            "Docker & Kubernetes",
            "Database Optimization",
            "Distributed Systems",
            "Security Best Practices"
        ]
    },
    "Data Analyst": {
        "core_skills": [
            "SQL",
            "Excel",
            "Python/R",
            "Data Visualization",
            "Statistical Analysis",
            "Data Cleaning",
            "Report Generation",
            "Business Intelligence Tools"
        ],
        "advanced_skills": [
            "Tableau/Power BI",
            "A/B Testing",
            "Predictive Analytics",
            "ETL Processes",
            "Data Warehousing",
            "Advanced Statistics",
            "Dashboard Design",
            "Stakeholder Communication"
        ]
    },
    "ML Engineer": {
        "core_skills": [
            "Python",
            "Machine Learning Algorithms",
            "Linear Algebra & Statistics",
            "Scikit-learn",
            "Data Preprocessing",
            "Model Evaluation",
            "SQL",
            "NumPy & Pandas"
        ],
        "advanced_skills": [
            "Deep Learning (TensorFlow/PyTorch)",
            "MLOps",
            "Model Deployment",
            "Feature Engineering",
            "Hyperparameter Tuning",
            "NLP/Computer Vision",
            "Distributed Training",
            "Cloud ML Services"
        ]
    }
}


def get_skills_for_role(role: str) -> dict:
    """
    Get skill set for a specific role.
    
    Args:
        role: Role name (SDE, Data Analyst, ML Engineer)
        
    Returns:
        Dictionary with core_skills and advanced_skills
    """
    return SKILL_SETS.get(role, SKILL_SETS["SDE"])


def get_all_skills_for_role(role: str) -> list:
    """
    Get combined list of all skills for a role.
    
    Args:
        role: Role name
        
    Returns:
        List of all skills (core + advanced)
    """
    skills = get_skills_for_role(role)
    return skills["core_skills"] + skills["advanced_skills"]


def get_available_roles() -> list:
    """Get list of all available roles."""
    return list(SKILL_SETS.keys())
