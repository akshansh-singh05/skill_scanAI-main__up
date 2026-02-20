"""
Resume Bullet Point Improver Service

Transforms weak resume bullet points into strong, impactful statements
with action verbs, metrics, and quantifiable achievements.
"""

import re
import random
from typing import Dict, List

# Strong action verbs by category
ACTION_VERBS = {
    "development": ["Developed", "Engineered", "Architected", "Built", "Designed", "Implemented", "Created", "Constructed"],
    "improvement": ["Optimized", "Enhanced", "Improved", "Streamlined", "Accelerated", "Boosted", "Elevated", "Refined"],
    "leadership": ["Led", "Spearheaded", "Directed", "Orchestrated", "Managed", "Coordinated", "Oversaw", "Supervised"],
    "analysis": ["Analyzed", "Evaluated", "Assessed", "Investigated", "Researched", "Examined", "Audited", "Diagnosed"],
    "automation": ["Automated", "Systematized", "Programmed", "Scripted", "Digitized", "Mechanized"],
    "collaboration": ["Collaborated", "Partnered", "Coordinated", "Integrated", "Unified", "Consolidated"],
}

# Tech-specific improvements
TECH_ENHANCEMENTS = {
    "react": ["React-based", "responsive", "component-driven", "dynamic"],
    "python": ["Python-powered", "scalable", "automated", "data-driven"],
    "javascript": ["JavaScript", "interactive", "real-time", "dynamic"],
    "node": ["Node.js", "server-side", "scalable", "event-driven"],
    "api": ["RESTful API", "microservices", "API-driven", "service-oriented"],
    "database": ["database", "data persistence", "optimized queries", "efficient storage"],
    "sql": ["SQL", "database-driven", "query-optimized", "relational"],
    "machine learning": ["ML-powered", "AI-driven", "predictive", "intelligent"],
    "aws": ["cloud-native", "AWS-hosted", "scalable infrastructure", "serverless"],
    "docker": ["containerized", "Docker-based", "portable", "microservices"],
}

# Metric templates
METRIC_TEMPLATES = [
    "improving {metric} by {percent}%",
    "resulting in {percent}% increase in {metric}",
    "achieving {percent}% improvement in {metric}",
    "reducing {negative_metric} by {percent}%",
    "enhancing {metric} {percent}%",
    "serving {number}+ users",
    "processing {number}+ requests daily",
    "handling {number}+ concurrent users",
]

METRICS = {
    "positive": ["performance", "efficiency", "user engagement", "productivity", "code quality", 
                 "test coverage", "response time", "throughput", "uptime", "user satisfaction",
                 "conversion rate", "load time", "UI responsiveness", "system reliability"],
    "negative": ["load time", "bug count", "deployment time", "downtime", "manual effort",
                 "processing time", "error rate", "latency", "technical debt"],
}


def detect_tech_stack(bullet: str) -> List[str]:
    """Detect technologies mentioned in the bullet point."""
    bullet_lower = bullet.lower()
    detected = []
    
    tech_keywords = {
        "react": ["react", "reactjs", "react.js"],
        "python": ["python", "django", "flask", "fastapi"],
        "javascript": ["javascript", "js", "typescript", "ts"],
        "node": ["node", "nodejs", "node.js", "express"],
        "api": ["api", "rest", "restful", "endpoint"],
        "database": ["database", "db", "mongodb", "postgresql", "mysql"],
        "sql": ["sql", "mysql", "postgresql", "sqlite"],
        "machine learning": ["ml", "machine learning", "ai", "model", "tensorflow", "pytorch"],
        "aws": ["aws", "amazon", "s3", "ec2", "lambda"],
        "docker": ["docker", "container", "kubernetes", "k8s"],
    }
    
    for tech, keywords in tech_keywords.items():
        if any(kw in bullet_lower for kw in keywords):
            detected.append(tech)
    
    return detected


def detect_action_category(bullet: str) -> str:
    """Detect the action category from the bullet point."""
    bullet_lower = bullet.lower()
    
    if any(word in bullet_lower for word in ["built", "created", "made", "developed", "wrote", "coded"]):
        return "development"
    elif any(word in bullet_lower for word in ["improved", "enhanced", "optimized", "fixed", "updated"]):
        return "improvement"
    elif any(word in bullet_lower for word in ["led", "managed", "supervised", "directed", "team"]):
        return "leadership"
    elif any(word in bullet_lower for word in ["analyzed", "researched", "studied", "evaluated"]):
        return "analysis"
    elif any(word in bullet_lower for word in ["automated", "scripted", "scheduled"]):
        return "automation"
    elif any(word in bullet_lower for word in ["worked with", "collaborated", "partnered", "helped"]):
        return "collaboration"
    
    return "development"  # Default


def generate_metric() -> str:
    """Generate a realistic metric statement."""
    template = random.choice(METRIC_TEMPLATES)
    
    if "{negative_metric}" in template:
        metric = random.choice(METRICS["negative"])
        percent = random.choice([15, 20, 25, 30, 35, 40, 45, 50])
        return template.format(negative_metric=metric, percent=percent)
    elif "{number}" in template:
        number = random.choice(["1K", "5K", "10K", "50K", "100K", "500K", "1M"])
        return template.format(number=number)
    else:
        metric = random.choice(METRICS["positive"])
        percent = random.choice([20, 25, 30, 35, 40, 45, 50, 60])
        return template.format(metric=metric, percent=percent)


def extract_core_subject(bullet: str) -> str:
    """Extract the main subject/object from the bullet point."""
    # Remove common weak starters
    weak_starters = [
        r"^(i |we |my |our )",
        r"^(worked on |helped with |was responsible for |did |made )",
        r"^(built |created |developed |wrote )",
    ]
    
    cleaned = bullet.strip()
    for pattern in weak_starters:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()


def improve_bullet(bullet: str, role: str = "SDE") -> Dict:
    """
    Transform a weak bullet point into a strong, impactful statement.
    
    Args:
        bullet: Original bullet point text
        role: Target role for context
        
    Returns:
        Dictionary with improved bullet and explanation
    """
    if not bullet or len(bullet.strip()) < 5:
        return {
            "original": bullet,
            "improved": bullet,
            "changes": [],
            "tips": ["Bullet point is too short to improve"]
        }
    
    # Detect context
    tech_stack = detect_tech_stack(bullet)
    action_category = detect_action_category(bullet)
    core_subject = extract_core_subject(bullet)
    
    # Select strong action verb
    action_verb = random.choice(ACTION_VERBS[action_category])
    
    # Build improved bullet
    improvements = []
    
    # Start with strong action verb
    improved = action_verb
    improvements.append(f"Added strong action verb: '{action_verb}'")
    
    # Add tech enhancements if applicable
    if tech_stack:
        tech = tech_stack[0]
        enhancement = random.choice(TECH_ENHANCEMENTS.get(tech, ["scalable"]))
        
        # Determine what was built
        if "website" in bullet.lower() or "web" in bullet.lower():
            improved += f" a {enhancement} web application"
        elif "app" in bullet.lower() or "application" in bullet.lower():
            improved += f" a {enhancement} application"
        elif "system" in bullet.lower():
            improved += f" a {enhancement} system"
        elif "api" in bullet.lower():
            improved += f" a {enhancement} API service"
        elif "feature" in bullet.lower():
            improved += f" {enhancement} features"
        elif "tool" in bullet.lower():
            improved += f" a {enhancement} tool"
        else:
            improved += f" a {enhancement} solution"
        
        improvements.append(f"Enhanced with technical descriptor: '{enhancement}'")
    else:
        # Generic improvement
        if "website" in bullet.lower():
            improved += " a scalable web platform"
        elif "app" in bullet.lower():
            improved += " a robust application"
        else:
            improved += " " + core_subject if core_subject else " an innovative solution"
    
    # Add quantifiable metric
    metric = generate_metric()
    improved += f", {metric}"
    improvements.append(f"Added quantifiable impact: '{metric}'")
    
    # Generate alternative versions
    alternatives = []
    for _ in range(2):
        alt_verb = random.choice([v for v in ACTION_VERBS[action_category] if v != action_verb])
        alt_metric = generate_metric()
        
        if tech_stack:
            tech = tech_stack[0]
            alt_enhancement = random.choice(TECH_ENHANCEMENTS.get(tech, ["efficient"]))
            if "website" in bullet.lower():
                alt = f"{alt_verb} a {alt_enhancement} web platform, {alt_metric}"
            else:
                alt = f"{alt_verb} a {alt_enhancement} solution, {alt_metric}"
        else:
            alt = f"{alt_verb} {core_subject}, {alt_metric}"
        
        alternatives.append(alt)
    
    # Tips for the user
    tips = [
        "Always start with a strong action verb",
        "Include quantifiable metrics when possible",
        "Mention specific technologies used",
        "Focus on impact and results, not just tasks",
        "Use numbers to demonstrate scale (users, %, time saved)",
    ]
    
    return {
        "original": bullet,
        "improved": improved,
        "alternatives": alternatives,
        "changes": improvements,
        "tips": random.sample(tips, 3),
        "tech_detected": tech_stack,
        "category": action_category
    }


def batch_improve_bullets(bullets: List[str], role: str = "SDE") -> List[Dict]:
    """Improve multiple bullet points at once."""
    return [improve_bullet(b, role) for b in bullets if b.strip()]
