from typing import Dict, List, Optional
import random
import re

from config.company_modes import get_company_config, get_company_questions, COMPANY_QUESTIONS


# Predefined question bank organized by role and difficulty
QUESTION_BANK = {
    "SDE": {
        "easy": [
            {
                "question": "What is the difference between an array and a linked list?",
                "keywords": ["array", "linked list", "memory", "access", "insertion", "contiguous", "pointer", "index"],
                "expected_points": ["memory allocation", "access time", "insertion/deletion"]
            },
            {
                "question": "Explain what a stack data structure is and give a real-world example.",
                "keywords": ["stack", "lifo", "push", "pop", "last in first out", "undo", "recursion"],
                "expected_points": ["LIFO principle", "operations", "use case"]
            },
            {
                "question": "What is the purpose of version control systems like Git?",
                "keywords": ["git", "version", "track", "changes", "collaborate", "branch", "merge", "history"],
                "expected_points": ["tracking changes", "collaboration", "branching"]
            },
            {
                "question": "What is an API and why is it important in software development?",
                "keywords": ["api", "interface", "communication", "request", "response", "integration", "service"],
                "expected_points": ["definition", "purpose", "examples"]
            },
            {
                "question": "Explain the concept of Object-Oriented Programming.",
                "keywords": ["oop", "class", "object", "inheritance", "encapsulation", "polymorphism", "abstraction"],
                "expected_points": ["four pillars", "class/object", "benefits"]
            }
        ],
        "medium": [
            {
                "question": "Explain the time complexity of common sorting algorithms.",
                "keywords": ["sort", "complexity", "o(n)", "quick", "merge", "bubble", "heap", "time", "space"],
                "expected_points": ["Big O notation", "comparison of algorithms", "best/worst cases"]
            },
            {
                "question": "What is the difference between SQL and NoSQL databases? When would you use each?",
                "keywords": ["sql", "nosql", "relational", "document", "schema", "scalability", "acid", "mongodb", "postgresql"],
                "expected_points": ["structure differences", "use cases", "trade-offs"]
            },
            {
                "question": "Explain how a hash table works and discuss collision handling.",
                "keywords": ["hash", "table", "collision", "chaining", "probing", "key", "value", "bucket", "function"],
                "expected_points": ["hashing mechanism", "collision strategies", "time complexity"]
            },
            {
                "question": "What is REST and what makes an API RESTful?",
                "keywords": ["rest", "stateless", "http", "resource", "endpoint", "get", "post", "put", "delete", "crud"],
                "expected_points": ["REST principles", "HTTP methods", "statelessness"]
            },
            {
                "question": "Describe the concept of recursion and when you would avoid using it.",
                "keywords": ["recursion", "base case", "stack", "overflow", "iteration", "memory", "call"],
                "expected_points": ["base case", "recursive case", "limitations"]
            }
        ],
        "hard": [
            {
                "question": "Design a URL shortening service like bit.ly. What components would you need?",
                "keywords": ["database", "hash", "redirect", "scale", "cache", "encoding", "base62", "analytics", "distributed"],
                "expected_points": ["architecture", "encoding strategy", "scalability", "storage"]
            },
            {
                "question": "Explain how you would handle concurrency issues in a multi-threaded application.",
                "keywords": ["thread", "lock", "mutex", "semaphore", "deadlock", "race condition", "synchronization", "atomic"],
                "expected_points": ["concurrency problems", "synchronization mechanisms", "best practices"]
            },
            {
                "question": "What are microservices and how do they differ from monolithic architecture?",
                "keywords": ["microservice", "monolith", "service", "deploy", "scale", "independent", "api", "docker", "kubernetes"],
                "expected_points": ["architectural differences", "pros/cons", "communication patterns"]
            },
            {
                "question": "Explain CAP theorem and its implications for distributed systems.",
                "keywords": ["cap", "consistency", "availability", "partition", "distributed", "trade-off", "tolerance"],
                "expected_points": ["three properties", "trade-offs", "real-world examples"]
            },
            {
                "question": "How would you design a rate limiter for an API?",
                "keywords": ["rate", "limit", "token", "bucket", "sliding", "window", "redis", "throttle", "algorithm"],
                "expected_points": ["algorithms", "storage", "distributed considerations"]
            }
        ]
    },
    "Data Analyst": {
        "easy": [
            {
                "question": "What is the difference between mean, median, and mode?",
                "keywords": ["mean", "median", "mode", "average", "central", "tendency", "outlier"],
                "expected_points": ["definitions", "when to use each", "outlier impact"]
            },
            {
                "question": "Explain what a JOIN operation does in SQL.",
                "keywords": ["join", "inner", "outer", "left", "right", "table", "combine", "key"],
                "expected_points": ["join types", "use cases", "syntax"]
            },
            {
                "question": "What is data cleaning and why is it important?",
                "keywords": ["clean", "missing", "duplicate", "outlier", "quality", "preprocessing", "null"],
                "expected_points": ["common issues", "importance", "techniques"]
            }
        ],
        "medium": [
            {
                "question": "Explain the concept of A/B testing and how you would design one.",
                "keywords": ["ab test", "hypothesis", "control", "variant", "significance", "sample", "conversion"],
                "expected_points": ["methodology", "statistical significance", "metrics"]
            },
            {
                "question": "What is the difference between correlation and causation?",
                "keywords": ["correlation", "causation", "relationship", "variable", "experiment", "confounding"],
                "expected_points": ["definitions", "examples", "avoiding mistakes"]
            },
            {
                "question": "How would you handle missing data in a dataset?",
                "keywords": ["missing", "imputation", "drop", "mean", "median", "interpolation", "null"],
                "expected_points": ["strategies", "trade-offs", "when to use each"]
            }
        ],
        "hard": [
            {
                "question": "Design a dashboard to track key business metrics. What would you include?",
                "keywords": ["dashboard", "kpi", "metric", "visualization", "stakeholder", "real-time", "filter"],
                "expected_points": ["metric selection", "visualization choices", "user needs"]
            },
            {
                "question": "Explain how you would detect anomalies in time series data.",
                "keywords": ["anomaly", "time series", "outlier", "seasonal", "trend", "statistical", "detection"],
                "expected_points": ["methods", "considerations", "handling seasonality"]
            }
        ]
    },
    "ML Engineer": {
        "easy": [
            {
                "question": "What is the difference between supervised and unsupervised learning?",
                "keywords": ["supervised", "unsupervised", "label", "classification", "clustering", "regression"],
                "expected_points": ["definitions", "examples", "use cases"]
            },
            {
                "question": "Explain what overfitting is and how to prevent it.",
                "keywords": ["overfit", "generalization", "regularization", "validation", "dropout", "cross-validation"],
                "expected_points": ["definition", "detection", "prevention techniques"]
            },
            {
                "question": "What is a training, validation, and test split?",
                "keywords": ["train", "validation", "test", "split", "evaluate", "generalization"],
                "expected_points": ["purpose of each", "typical ratios", "importance"]
            }
        ],
        "medium": [
            {
                "question": "Explain the bias-variance tradeoff in machine learning.",
                "keywords": ["bias", "variance", "tradeoff", "underfit", "overfit", "complexity", "error"],
                "expected_points": ["definitions", "relationship", "balancing"]
            },
            {
                "question": "What are gradient descent and its variants?",
                "keywords": ["gradient", "descent", "learning rate", "sgd", "batch", "mini-batch", "adam", "optimization"],
                "expected_points": ["algorithm", "variants", "hyperparameters"]
            },
            {
                "question": "How do you handle imbalanced datasets in classification?",
                "keywords": ["imbalance", "oversample", "undersample", "smote", "weight", "precision", "recall"],
                "expected_points": ["techniques", "metrics", "trade-offs"]
            }
        ],
        "hard": [
            {
                "question": "Explain how transformers work and their advantage over RNNs.",
                "keywords": ["transformer", "attention", "rnn", "parallel", "sequence", "encoder", "decoder", "self-attention"],
                "expected_points": ["attention mechanism", "parallelization", "architecture"]
            },
            {
                "question": "How would you deploy a machine learning model to production?",
                "keywords": ["deploy", "api", "docker", "kubernetes", "monitoring", "inference", "latency", "scale"],
                "expected_points": ["deployment strategies", "monitoring", "scaling"]
            },
            {
                "question": "Explain the concept of feature importance and how to compute it.",
                "keywords": ["feature", "importance", "permutation", "shap", "gain", "interpretability", "coefficient"],
                "expected_points": ["methods", "interpretation", "limitations"]
            }
        ]
    }
}


def generate_question(role: str, difficulty: str = "medium") -> Dict:
    """
    Generate an interview question based on role and difficulty.
    
    Args:
        role: Target role (SDE, Data Analyst, ML Engineer)
        difficulty: Question difficulty (easy, medium, hard)
        
    Returns:
        Dictionary with question details
    """
    # Normalize inputs
    difficulty = difficulty.lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "medium"
    
    # Get question bank for role
    role_questions = QUESTION_BANK.get(role, QUESTION_BANK["SDE"])
    difficulty_questions = role_questions.get(difficulty, role_questions["medium"])
    
    # Select random question
    question_data = random.choice(difficulty_questions)
    
    return {
        "question": question_data["question"],
        "difficulty": difficulty,
        "role": role,
        "keywords": question_data["keywords"],
        "expected_points": question_data["expected_points"]
    }


def generate_company_question(role: str, difficulty: str = "medium", company: str = "generic") -> Dict:
    """
    Generate a company-specific interview question.
    
    Args:
        role: Target role (SDE, Data Analyst, ML Engineer)
        difficulty: Question difficulty (easy, medium, hard)
        company: Company mode (google, amazon, meta, etc.)
        
    Returns:
        Dictionary with question details adapted for company style
    """
    company_config = get_company_config(company)
    company_qs = COMPANY_QUESTIONS.get(company.lower(), {})
    
    # Determine question type based on company distribution
    distribution = company_config.get("question_distribution", {})
    question_type = _select_question_type(distribution)
    
    # Try to get company-specific question
    if company_qs and question_type in company_qs:
        type_questions = company_qs[question_type]
        if type_questions:
            q = random.choice(type_questions)
            return _format_company_question(q, question_type, difficulty, role, company_config)
    
    # Fall back to standard questions with company-style modifications
    base_question = generate_question(role, difficulty)
    return _adapt_question_to_company(base_question, company_config, question_type)


def _select_question_type(distribution: Dict[str, float]) -> str:
    """Select question type based on probability distribution."""
    if not distribution:
        return "coding"
    
    rand = random.random()
    cumulative = 0
    
    for qtype, prob in distribution.items():
        cumulative += prob
        if rand <= cumulative:
            return qtype
    
    return list(distribution.keys())[0]


def _format_company_question(
    question_data: Dict,
    question_type: str,
    difficulty: str,
    role: str,
    company_config: Dict
) -> Dict:
    """Format a company-specific question."""
    result = {
        "question": question_data.get("question", ""),
        "difficulty": question_data.get("difficulty", difficulty),
        "role": role,
        "question_type": question_type,
        "company": company_config["name"],
        "company_style": company_config["style"],
    }
    
    # Add type-specific fields
    if question_type == "behavioral":
        result["principle"] = question_data.get("principle", "")
        result["star_prompts"] = question_data.get("star_prompts", [])
        result["keywords"] = [question_data.get("principle", "").lower(), "star", "situation", "action", "result"]
        result["expected_points"] = ["specific example", "clear actions taken", "measurable results"]
    else:
        result["keywords"] = question_data.get("topics", ["problem solving", "optimization", "clarity"])
        result["expected_points"] = question_data.get("topics", ["approach", "implementation", "complexity"])
        result["follow_up"] = question_data.get("follow_up", "")
    
    return result


def _adapt_question_to_company(base_question: Dict, company_config: Dict, question_type: str) -> Dict:
    """Adapt a standard question to company style."""
    question = base_question.copy()
    
    company_name = company_config["name"]
    style = company_config["style"]
    
    # Add company context
    question["company"] = company_name
    question["company_style"] = style
    question["question_type"] = question_type
    
    # Modify question based on company style
    if style == "dsa_heavy" and "optimize" not in question["question"].lower():
        question["question"] += " What is the optimal time and space complexity?"
    elif style == "leadership_behavioral":
        if question_type != "behavioral":
            question["question"] += " Also, tell me about a time you faced a similar challenge."
    elif style == "coding_systems":
        if "scale" not in question["question"].lower():
            question["question"] += " How would this work at massive scale?"
    
    return question


def evaluate_answer(
    question: str,
    answer: str,
    difficulty: str,
    role: str,
    keywords: Optional[List[str]] = None
) -> Dict:
    """
    Evaluate an interview answer using heuristics.
    Designed to be extendable for LLM integration.
    
    Args:
        question: The interview question
        answer: User's answer
        difficulty: Question difficulty
        role: Target role
        keywords: Expected keywords (optional, will lookup if not provided)
        
    Returns:
        Evaluation results with score and feedback
    """
    # Get keywords if not provided
    if keywords is None:
        keywords = _get_keywords_for_question(question, role, difficulty)
    
    answer_lower = answer.lower()
    
    # Evaluation criteria
    length_score = _evaluate_length(answer, difficulty)
    keyword_score = _evaluate_keywords(answer_lower, keywords)
    structure_score = _evaluate_structure(answer)
    
    # Weighted total (can be adjusted)
    total_score = int(
        length_score * 0.2 +
        keyword_score * 0.5 +
        structure_score * 0.3
    )
    
    # Ensure score is within bounds
    total_score = max(0, min(100, total_score))
    
    # Generate feedback
    feedback = _generate_feedback(length_score, keyword_score, structure_score, keywords, answer_lower)
    
    # Determine next difficulty
    next_difficulty = _determine_next_difficulty(total_score, difficulty)
    
    return {
        "question": question,
        "evaluation_score": total_score,
        "feedback": feedback,
        "next_difficulty": next_difficulty,
        "breakdown": {
            "length_score": length_score,
            "keyword_score": keyword_score,
            "structure_score": structure_score
        }
    }


def _evaluate_length(answer: str, difficulty: str) -> int:
    """Evaluate answer length appropriateness."""
    word_count = len(answer.split())
    
    # Expected length ranges by difficulty
    ranges = {
        "easy": (30, 150),
        "medium": (50, 250),
        "hard": (80, 400)
    }
    
    min_words, max_words = ranges.get(difficulty, (50, 250))
    
    if word_count < 5:
        return 5  # Way too short - almost no answer
    elif word_count < 10:
        return 10  # Very short answer
    elif word_count < min_words // 2:
        return 20  # Too short
    elif word_count < min_words:
        return 45  # Somewhat short
    elif word_count <= max_words:
        return 100  # Good length
    elif word_count <= max_words * 1.5:
        return 75  # Slightly long but acceptable
    else:
        return 50  # Too verbose


def _evaluate_keywords(answer_lower: str, keywords: List[str]) -> int:
    """Evaluate presence of expected technical keywords."""
    if not keywords:
        return 30  # Default score if no keywords - be conservative
    
    found = 0
    for keyword in keywords:
        if keyword.lower() in answer_lower:
            found += 1
    
    percentage = (found / len(keywords)) * 100
    return int(percentage)


def _evaluate_structure(answer: str) -> int:
    """Evaluate logical structure of the answer."""
    score = 20  # Lower base score - structure must be earned
    
    # Check for structured elements
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Very few sentences = poor structure
    if len(sentences) < 2:
        return 10 if len(sentences) == 1 else 5
    
    # Multiple sentences indicate structure
    if len(sentences) >= 4:
        score += 25
    elif len(sentences) >= 3:
        score += 15
    elif len(sentences) >= 2:
        score += 10
    
    # Check for transition words (indicates logical flow)
    transition_words = [
        "first", "second", "third", "finally", "however", "therefore",
        "for example", "additionally", "moreover", "in conclusion",
        "because", "since", "as a result", "on the other hand"
    ]
    
    answer_lower = answer.lower()
    transitions_found = sum(1 for word in transition_words if word in answer_lower)
    
    if transitions_found >= 3:
        score += 25
    elif transitions_found >= 2:
        score += 15
    elif transitions_found >= 1:
        score += 10
    
    # Check for examples
    if "example" in answer_lower or "for instance" in answer_lower:
        score += 15
    
    # Check for gibberish - random characters with no real words
    words = answer.split()
    if words:
        # Simple gibberish detection: check if words have mostly consonants or random chars
        gibberish_word_count = 0
        common_words = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "it", "this", "that", "i", "we", "you", "they", "my", "your", "can", "will", "be", "have", "has", "do", "does", "not", "from", "by", "as", "if", "so", "what", "how", "why", "when", "where", "which"}
        real_word_count = sum(1 for w in words if w.lower() in common_words or (len(w) > 2 and w.isalpha()))
        if real_word_count / len(words) < 0.5:
            score = max(5, score - 30)  # Heavy penalty for gibberish
    
    return min(100, score)


def _get_keywords_for_question(question: str, role: str, difficulty: str) -> List[str]:
    """Look up keywords for a given question."""
    role_questions = QUESTION_BANK.get(role, QUESTION_BANK["SDE"])
    difficulty_questions = role_questions.get(difficulty, role_questions["medium"])
    
    for q_data in difficulty_questions:
        if q_data["question"] == question:
            return q_data["keywords"]
    
    return []


def _generate_feedback(
    length_score: int,
    keyword_score: int,
    structure_score: int,
    keywords: List[str],
    answer_lower: str
) -> str:
    """Generate human-readable feedback."""
    feedback_parts = []
    
    # Length feedback
    if length_score < 50:
        feedback_parts.append("Your answer is too brief. Try to elaborate more with examples and explanations.")
    elif length_score >= 90:
        feedback_parts.append("Good answer length.")
    
    # Keyword feedback
    if keyword_score < 40:
        missing = [k for k in keywords[:3] if k.lower() not in answer_lower]
        if missing:
            feedback_parts.append(f"Consider mentioning key concepts like: {', '.join(missing)}.")
    elif keyword_score >= 70:
        feedback_parts.append("Good coverage of relevant technical concepts.")
    
    # Structure feedback
    if structure_score < 50:
        feedback_parts.append("Try to structure your answer with clear points and examples.")
    elif structure_score >= 80:
        feedback_parts.append("Well-structured response.")
    
    # Overall feedback
    avg_score = (length_score + keyword_score + structure_score) / 3
    if avg_score >= 80:
        feedback_parts.append("Excellent answer overall!")
    elif avg_score >= 60:
        feedback_parts.append("Good answer with room for improvement.")
    elif avg_score >= 40:
        feedback_parts.append("Adequate answer but needs more depth.")
    else:
        feedback_parts.append("Review the core concepts and practice explaining them clearly.")
    
    return " ".join(feedback_parts)


def _determine_next_difficulty(score: int, current_difficulty: str) -> str:
    """Determine next question difficulty based on performance."""
    if score >= 80:
        # Increase difficulty
        if current_difficulty == "easy":
            return "medium"
        elif current_difficulty == "medium":
            return "hard"
        else:
            return "hard"
    elif score >= 50:
        # Stay at same level
        return current_difficulty
    else:
        # Decrease difficulty
        if current_difficulty == "hard":
            return "medium"
        elif current_difficulty == "medium":
            return "easy"
        else:
            return "easy"


# LLM Integration placeholder
async def evaluate_answer_with_llm(
    question: str,
    answer: str,
    difficulty: str,
    role: str,
    llm_client=None
) -> Dict:
    """
    Evaluate answer using LLM for more nuanced feedback.
    Placeholder for future LLM integration.
    
    Args:
        question: Interview question
        answer: User's answer
        difficulty: Question difficulty
        role: Target role
        llm_client: LLM client instance (e.g., OpenAI)
        
    Returns:
        Evaluation results
    """
    if llm_client is None:
        # Fall back to heuristic evaluation
        return evaluate_answer(question, answer, difficulty, role)
    
    # TODO: Implement LLM-based evaluation
    # prompt = f"""
    # Evaluate the following interview answer:
    # Role: {role}
    # Difficulty: {difficulty}
    # Question: {question}
    # Answer: {answer}
    # 
    # Provide:
    # 1. Score (0-100)
    # 2. Detailed feedback
    # 3. Suggested next difficulty
    # """
    # response = await llm_client.complete(prompt)
    # return parse_llm_response(response)
    
    return evaluate_answer(question, answer, difficulty, role)
