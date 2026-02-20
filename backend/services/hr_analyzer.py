from typing import Dict, List
import re
import string


# Leadership and confidence keywords
CONFIDENCE_KEYWORDS = [
    "led", "lead", "managed", "directed", "spearheaded", "initiated",
    "achieved", "accomplished", "delivered", "exceeded", "surpassed",
    "improved", "increased", "reduced", "optimized", "transformed",
    "responsible", "ownership", "accountable", "drove", "championed",
    "successfully", "effectively", "efficiently", "proactively",
    "decided", "determined", "resolved", "solved", "overcame"
]

LEADERSHIP_KEYWORDS = [
    "team", "collaborated", "coordinated", "mentored", "coached",
    "delegated", "motivated", "inspired", "influenced", "persuaded",
    "negotiated", "facilitated", "organized", "supervised", "trained",
    "led", "leadership", "cross-functional", "stakeholder", "consensus"
]

# STAR method indicators
STAR_INDICATORS = {
    "situation": [
        "situation", "context", "background", "scenario", "challenge",
        "problem", "issue", "when", "while working", "at my previous",
        "in my role", "during", "faced with"
    ],
    "task": [
        "task", "responsibility", "goal", "objective", "assigned",
        "needed to", "had to", "required to", "expected to", "my role was",
        "i was responsible", "charged with"
    ],
    "action": [
        "action", "i did", "i took", "implemented", "developed", "created",
        "designed", "built", "established", "initiated", "executed",
        "i decided", "i started", "i began", "my approach", "steps i took"
    ],
    "result": [
        "result", "outcome", "impact", "achieved", "accomplished",
        "led to", "resulted in", "consequently", "as a result", "ultimately",
        "success", "improved", "increased", "reduced", "saved", "delivered"
    ]
}

# Question-specific relevance keywords
QUESTION_RELEVANCE_MAP = {
    "challenge": ["challenge", "difficult", "hard", "problem", "obstacle", "struggle", "issue", "tough", "overcome"],
    "difficult team member": ["team", "colleague", "coworker", "conflict", "disagreement", "difficult person", "communication"],
    "leadership": ["lead", "led", "team", "managed", "directed", "initiative", "guided", "motivated", "inspired"],
    "failed": ["fail", "mistake", "error", "wrong", "learned", "lesson", "setback", "didn't work"],
    "deadline": ["deadline", "time", "urgent", "quick", "fast", "pressure", "rushed", "days", "hours", "weeks"],
    "above and beyond": ["extra", "beyond", "more than", "additional", "volunteered", "initiative", "own time"],
    "persuade": ["persuade", "convince", "argument", "presented", "explained", "showed", "demonstrated", "negotiated"],
    "feedback": ["feedback", "criticism", "critique", "review", "told me", "suggested", "improved", "changed"]
}

# Red flags - things that indicate a poor/fake answer
RED_FLAG_PATTERNS = [
    r"asdf", r"qwerty", r"zxcv", r"jkl", r";\s*;\s*;",  # Keyboard mashing
    r"(.)\1{4,}",  # Repeated characters (aaaaa, bbbbb)
    r"test\s*test", r"hello\s*hello", r"blah\s*blah",  # Test/placeholder text
    r"^(yes|no|ok|okay|sure|fine|good|bad|idk|dunno)\.?$",  # One-word answers
    r"lorem ipsum",  # Placeholder text
    r"i don'?t know", r"no idea", r"not sure",  # Admission of not knowing
]

# Generic/vague phrases that show lack of specifics
VAGUE_PHRASES = [
    "i worked hard", "i did my best", "i tried", "we worked together",
    "it was difficult", "i managed it", "things worked out", "it went well",
    "i handled it", "i dealt with it", "we figured it out", "i made it happen",
    "i was successful", "good results", "positive outcome", "everything was fine"
]

# Hedging/uncertainty words
HEDGING_WORDS = [
    "maybe", "perhaps", "i think", "i guess", "sort of", "kind of",
    "probably", "might have", "could have", "possibly", "somewhat",
    "i believe", "i feel like", "in a way", "more or less"
]

# Off-topic red flags
OFF_TOPIC_PHRASES = [
    "what was the question", "can you repeat", "i forgot",
    "anyway", "by the way", "unrelated but", "off topic"
]


def detect_gibberish(text: str) -> Dict[str, any]:
    """
    Detect if text is gibberish, random, or spam.
    Returns detection results with severity.
    """
    text_lower = text.lower()
    
    issues = []
    severity = 0  # 0 = none, 1 = minor, 2 = moderate, 3 = severe
    
    # Check for red flag patterns
    for pattern in RED_FLAG_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            issues.append("Contains random or placeholder text")
            severity = max(severity, 3)
            break
    
    # Check character diversity (gibberish often has low diversity)
    unique_chars = len(set(text_lower.replace(" ", "")))
    total_chars = len(text_lower.replace(" ", ""))
    if total_chars > 20 and unique_chars < 8:
        issues.append("Very low character diversity - appears random")
        severity = max(severity, 3)
    
    # Check for excessive punctuation
    punct_count = sum(1 for c in text if c in string.punctuation)
    if len(text) > 10 and punct_count / len(text) > 0.3:
        issues.append("Excessive punctuation")
        severity = max(severity, 2)
    
    # Check for too many numbers (unless discussing metrics)
    digit_ratio = sum(1 for c in text if c.isdigit()) / max(len(text), 1)
    if digit_ratio > 0.3 and "%" not in text and "$" not in text:
        issues.append("Excessive numbers without context")
        severity = max(severity, 2)
    
    # Check word repetition (same word > 5 times)
    words = text_lower.split()
    if words:
        word_counts = {}
        for word in words:
            if len(word) > 2:
                word_counts[word] = word_counts.get(word, 0) + 1
        max_repetition = max(word_counts.values()) if word_counts else 0
        if max_repetition > 5 and len(words) < 50:
            issues.append("Excessive word repetition")
            severity = max(severity, 2)
    
    # Check average word length (gibberish often has weird lengths)
    if words:
        avg_word_len = sum(len(w) for w in words) / len(words)
        if avg_word_len > 12 or avg_word_len < 2:
            issues.append("Unusual word patterns")
            severity = max(severity, 2)
    
    return {
        "is_gibberish": severity >= 2,
        "severity": severity,
        "issues": issues
    }


def check_answer_relevance(question: str, answer: str) -> Dict[str, any]:
    """
    Check if the answer is relevant to the question asked.
    """
    question_lower = question.lower()
    answer_lower = answer.lower()
    
    issues = []
    relevance_score = 5  # Start neutral
    
    # Detect question type
    question_type = None
    for q_type, keywords in QUESTION_RELEVANCE_MAP.items():
        if any(kw in question_lower for kw in keywords):
            question_type = q_type
            break
    
    # Check if answer addresses the question type
    if question_type:
        relevant_keywords = QUESTION_RELEVANCE_MAP[question_type]
        matches = sum(1 for kw in relevant_keywords if kw in answer_lower)
        
        if matches == 0:
            issues.append(f"Answer doesn't address the '{question_type}' aspect of the question")
            relevance_score -= 3
        elif matches >= 2:
            relevance_score += 2
    
    # Check for off-topic indicators
    for phrase in OFF_TOPIC_PHRASES:
        if phrase in answer_lower:
            issues.append("Contains off-topic indicators")
            relevance_score -= 2
            break
    
    # Check if answer is actually telling a story/example
    story_indicators = ["when", "once", "time", "example", "project", "company", "role", "job"]
    has_story = any(ind in answer_lower for ind in story_indicators)
    
    if not has_story and len(answer.split()) > 20:
        issues.append("Doesn't provide a specific example or story")
        relevance_score -= 2
    
    # Check for generic non-answers
    generic_starts = [
        "i am a hard worker", "i always try", "i believe in", "i am passionate",
        "communication is important", "teamwork is essential", "i am dedicated"
    ]
    for phrase in generic_starts:
        if answer_lower.startswith(phrase) or f". {phrase}" in answer_lower:
            issues.append("Uses generic statements instead of specific examples")
            relevance_score -= 2
            break
    
    return {
        "relevance_score": max(0, min(10, relevance_score)),
        "question_type": question_type,
        "issues": issues,
        "is_relevant": relevance_score >= 4
    }


def detect_red_flags(answer: str) -> List[str]:
    """
    Detect interview red flags that would concern a real interviewer.
    """
    answer_lower = answer.lower()
    red_flags = []
    
    # Blaming others
    blame_patterns = [
        "it was their fault", "they made me", "not my fault", "blame",
        "they didn't", "my manager was bad", "my team was incompetent",
        "no one helped me", "they were useless"
    ]
    if any(p in answer_lower for p in blame_patterns):
        red_flags.append("Blames others instead of taking accountability - major red flag in big tech interviews")
    
    # Negative attitude
    negative_patterns = [
        "i hate", "i hated", "stupid", "dumb", "worst", "terrible company",
        "bad manager", "toxic", "the company was awful"
    ]
    if any(p in answer_lower for p in negative_patterns):
        red_flags.append("Displays negative attitude about previous employers - interviewers note this")
    
    # No ownership
    we_count = answer_lower.count(" we ")
    i_count = answer_lower.count(" i ")
    if we_count > 5 and i_count < 2:
        red_flags.append("Uses 'we' excessively without clarifying your individual contribution")
    
    # Vague about results
    has_result_keywords = any(kw in answer_lower for kw in STAR_INDICATORS["result"])
    has_numbers = bool(re.search(r'\d+%?', answer))
    
    word_count = len(answer.split())
    if word_count > 50 and not has_result_keywords:
        red_flags.append("Long answer with no clear outcome or result mentioned")
    
    if has_result_keywords and not has_numbers and word_count > 30:
        red_flags.append("Claims results but provides no quantifiable metrics (%, $, time saved, etc.)")
    
    # Too short for behavioral question
    if word_count < 30:
        red_flags.append("Response is too brief for a behavioral question - shows lack of depth or preparation")
    
    # Hedging too much
    hedge_count = sum(1 for h in HEDGING_WORDS if h in answer_lower)
    if hedge_count >= 3:
        red_flags.append("Excessive hedging language undermines confidence")
    
    # Vague phrases
    vague_count = sum(1 for v in VAGUE_PHRASES if v in answer_lower)
    if vague_count >= 2:
        red_flags.append("Uses vague phrases without concrete details - interviewers want specifics")
    
    return red_flags


def analyze_hr_response(answer: str, question: str = "") -> Dict:
    """
    Analyze HR behavioral interview response with strict validation.
    
    Args:
        answer: User's response to HR question
        question: The question asked (optional, for relevance checking)
        
    Returns:
        Analysis with clarity, confidence, structure scores and feedback
    """
    answer_lower = answer.lower()
    
    # First, check for gibberish/spam
    gibberish_check = detect_gibberish(answer)
    if gibberish_check["is_gibberish"]:
        return {
            "clarity": 1,
            "confidence": 1,
            "structure": 1,
            "feedback": generate_rejection_feedback(gibberish_check["issues"]),
            "total_score": 1,
            "is_valid": False,
            "rejection_reason": "Invalid response detected",
            "details": {
                "star_components_found": {},
                "confidence_keywords_found": 0,
                "leadership_keywords_found": 0,
                "red_flags": gibberish_check["issues"]
            }
        }
    
    # Check relevance if question provided
    relevance_result = None
    if question:
        relevance_result = check_answer_relevance(question, answer)
    
    # Detect red flags
    red_flags = detect_red_flags(answer)
    
    # Evaluate each component
    clarity_score = evaluate_clarity(answer)
    confidence_score = evaluate_confidence(answer_lower)
    structure_score = evaluate_star_structure(answer_lower)
    
    # Apply penalties for red flags
    red_flag_penalty = min(len(red_flags) * 1.5, 5)  # Max 5 point penalty
    
    # Apply relevance penalty
    relevance_penalty = 0
    if relevance_result and not relevance_result["is_relevant"]:
        relevance_penalty = 3
    
    # Adjust scores
    clarity_score = max(1, clarity_score - int(red_flag_penalty / 2))
    confidence_score = max(1, confidence_score - int(red_flag_penalty / 2))
    structure_score = max(1, structure_score - relevance_penalty)
    
    total_score = int((clarity_score + confidence_score + structure_score) / 3)
    
    # Generate feedback
    feedback = generate_hr_feedback(
        clarity_score, confidence_score, structure_score,
        answer_lower, red_flags, relevance_result
    )
    
    return {
        "clarity": clarity_score,
        "confidence": confidence_score,
        "structure": structure_score,
        "feedback": feedback,
        "total_score": total_score,
        "is_valid": True,
        "details": {
            "star_components_found": detect_star_components(answer_lower),
            "confidence_keywords_found": count_confidence_keywords(answer_lower),
            "leadership_keywords_found": count_leadership_keywords(answer_lower),
            "red_flags": red_flags,
            "relevance_issues": relevance_result["issues"] if relevance_result else []
        }
    }


def evaluate_clarity(answer: str) -> int:
    """
    Evaluate answer clarity based on sentence structure.
    Score out of 10.
    """
    # Check for very short or empty answers
    word_count = len(answer.split())
    if word_count < 5:
        return 1  # Way too short
    if word_count < 10:
        return 2  # Very short
    if word_count < 20:
        return 3  # Still too brief for HR answer
    
    score = 3  # Lower base score - clarity must be earned
    
    # Split into sentences
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 1
    
    if len(sentences) < 2:
        return 2  # Single sentence - poor clarity
    
    # Calculate average sentence length
    avg_words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences)
    
    # Optimal sentence length is 15-25 words
    if 10 <= avg_words_per_sentence <= 25:
        score += 4
    elif 8 <= avg_words_per_sentence <= 30:
        score += 2
    elif avg_words_per_sentence > 40:
        score -= 1  # Too long, hard to follow
    elif avg_words_per_sentence < 5:
        score -= 1  # Too choppy
    
    # Check for run-on sentences (very long sentences)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 40)
    if long_sentences == 0 and len(sentences) >= 3:
        score += 2
    
    # Check for proper sentence variation
    if len(sentences) >= 4:
        lengths = [len(s.split()) for s in sentences]
        variation = max(lengths) - min(lengths)
        if variation > 5:  # Good variation
            score += 1
    
    return max(1, min(10, score))


def evaluate_confidence(answer_lower: str) -> int:
    """
    Evaluate confidence based on keyword presence.
    Score out of 10.
    """
    # Check for very short answers
    word_count = len(answer_lower.split())
    if word_count < 10:
        return 2  # Can't show confidence in very short answer
    if word_count < 20:
        return 3
    
    score = 2  # Lower base score - confidence must be demonstrated
    
    # Count confidence keywords
    confidence_count = count_confidence_keywords(answer_lower)
    leadership_count = count_leadership_keywords(answer_lower)
    
    total_keywords = confidence_count + leadership_count
    
    # Award points based on keyword density
    if total_keywords >= 8:
        score += 5
    elif total_keywords >= 5:
        score += 4
    elif total_keywords >= 3:
        score += 3
    elif total_keywords >= 2:
        score += 2
    elif total_keywords >= 1:
        score += 1
    
    # Check for first-person ownership
    first_person_patterns = ["i led", "i managed", "i decided", "i took", "my decision", "i initiated"]
    ownership_count = sum(1 for p in first_person_patterns if p in answer_lower)
    
    if ownership_count >= 3:
        score += 2
    elif ownership_count >= 1:
        score += 1
    
    # Penalize hedging language
    hedging_words = ["maybe", "perhaps", "i think", "i guess", "sort of", "kind of", "probably"]
    hedge_count = sum(1 for h in hedging_words if h in answer_lower)
    
    if hedge_count >= 3:
        score -= 3
    elif hedge_count >= 1:
        score -= 1
    
    return max(1, min(10, score))


def evaluate_star_structure(answer_lower: str) -> int:
    """
    Evaluate STAR method structure presence.
    Score out of 10.
    """
    # Check for very short answers - can't have structure
    word_count = len(answer_lower.split())
    if word_count < 10:
        return 1
    if word_count < 20:
        return 2
    
    components_found = detect_star_components(answer_lower)
    components_count = sum(components_found.values())
    
    # Score based on STAR components
    if components_count == 4:
        score = 10
    elif components_count == 3:
        score = 7
    elif components_count == 2:
        score = 4
    elif components_count == 1:
        score = 2
    else:
        score = 1  # No STAR components = very poor structure
    
    # Bonus for having both Situation and Result (key bookends)
    if components_found.get("situation") and components_found.get("result"):
        score = min(10, score + 1)
    
    return score


def detect_star_components(answer_lower: str) -> Dict[str, bool]:
    """Detect which STAR components are present."""
    components = {}
    
    for component, indicators in STAR_INDICATORS.items():
        found = any(indicator in answer_lower for indicator in indicators)
        components[component] = found
    
    return components


def count_confidence_keywords(answer_lower: str) -> int:
    """Count confidence keywords in answer."""
    return sum(1 for keyword in CONFIDENCE_KEYWORDS if keyword in answer_lower)


def count_leadership_keywords(answer_lower: str) -> int:
    """Count leadership keywords in answer."""
    return sum(1 for keyword in LEADERSHIP_KEYWORDS if keyword in answer_lower)


def generate_rejection_feedback(issues: List[str]) -> str:
    """Generate feedback for invalid/gibberish responses."""
    return (
        "This response cannot be evaluated. " +
        " ".join(issues) + " " +
        "In a real interview at companies like Google, Amazon, or Microsoft, "
        "this type of response would immediately disqualify you. "
        "Please provide a genuine, thoughtful answer that describes a specific situation from your experience."
    )


def generate_hr_feedback(
    clarity: int,
    confidence: int,
    structure: int,
    answer_lower: str,
    red_flags: List[str] = None,
    relevance_result: Dict = None
) -> str:
    """
    Generate realistic, tough but constructive feedback like big tech interviewers.
    This feedback is honest and points out real issues.
    """
    red_flags = red_flags or []
    feedback_parts = []
    avg_score = (clarity + confidence + structure) / 3
    
    # CRITICAL: Address red flags first (dealbreakers in real interviews)
    if red_flags:
        feedback_parts.append("🚨 CRITICAL ISSUES DETECTED:")
        for flag in red_flags[:3]:  # Show top 3 issues
            feedback_parts.append(f"• {flag}")
        feedback_parts.append("")
    
    # Address relevance issues
    if relevance_result and relevance_result.get("issues"):
        feedback_parts.append("⚠️ RELEVANCE CONCERNS:")
        for issue in relevance_result["issues"][:2]:
            feedback_parts.append(f"• {issue}")
        feedback_parts.append("")
    
    # Structure feedback - Big tech cares about STAR
    components = detect_star_components(answer_lower)
    missing_components = [k.upper() for k, v in components.items() if not v]
    present_components = [k.upper() for k, v in components.items() if v]
    
    feedback_parts.append("📋 STRUCTURE ANALYSIS:")
    if structure >= 8:
        feedback_parts.append("• Strong STAR method execution. All components clearly present.")
    elif structure >= 5:
        feedback_parts.append(f"• Partial STAR structure detected. Found: {', '.join(present_components) if present_components else 'None'}.")
        if missing_components:
            feedback_parts.append(f"• Missing: {', '.join(missing_components)}. At Google/Amazon, incomplete STAR = incomplete answer.")
    elif structure >= 3:
        feedback_parts.append("• Weak structure. Your answer rambles without clear organization.")
        feedback_parts.append(f"• Missing STAR components: {', '.join(missing_components)}.")
        feedback_parts.append("• Big tech interviewers are trained to detect missing structure - this would hurt your scorecard.")
    else:
        feedback_parts.append("• No discernible STAR structure. This is a fundamental requirement for behavioral interviews.")
        feedback_parts.append("• At companies like Meta, Microsoft, or Amazon, this answer would receive a 'Not Inclined' rating.")
    feedback_parts.append("")
    
    # Confidence/Ownership feedback
    feedback_parts.append("💪 OWNERSHIP & CONFIDENCE:")
    we_count = answer_lower.count(" we ")
    i_count = answer_lower.count(" i ")
    
    if confidence >= 8:
        feedback_parts.append("• Good use of first-person ownership. You clearly articulated your individual contributions.")
    elif confidence >= 5:
        if we_count > i_count:
            feedback_parts.append("• Too much 'we' and not enough 'I'. Interviewers want to know what YOU did, not your team.")
            feedback_parts.append("• Hiring managers will ask: 'But what was YOUR specific contribution?'")
        else:
            feedback_parts.append("• Moderate confidence shown. Add more action verbs (led, drove, delivered, achieved).")
    elif confidence >= 3:
        feedback_parts.append("• Weak ownership demonstrated. You sound unsure of your own contributions.")
        feedback_parts.append("• Hedging words like 'maybe', 'I think', 'sort of' undermine your credibility.")
    else:
        feedback_parts.append("• Poor confidence projection. In a real interview, this would raise doubts about your capabilities.")
        feedback_parts.append("• Senior interviewers specifically look for candidates who can clearly articulate their impact.")
    feedback_parts.append("")
    
    # Clarity feedback
    feedback_parts.append("🎯 CLARITY & COMMUNICATION:")
    if clarity >= 8:
        feedback_parts.append("• Clear, well-structured sentences. Easy to follow your narrative.")
    elif clarity >= 5:
        feedback_parts.append("• Acceptable clarity but could be sharper. Aim for concise, punchy sentences.")
        feedback_parts.append("• Remember: interviewers are evaluating 5-8 candidates. Make your points memorable.")
    elif clarity >= 3:
        feedback_parts.append("• Unclear communication. Sentences are either too long or too choppy.")
        feedback_parts.append("• Practice the 'headline + details' approach: state your point, then elaborate.")
    else:
        feedback_parts.append("• Very poor clarity. Hard to understand your main points.")
        feedback_parts.append("• This would be flagged as a communication concern in interviewer feedback.")
    feedback_parts.append("")
    
    # Check for specific improvements needed
    has_metrics = bool(re.search(r'\d+%?', answer_lower))
    if not has_metrics and avg_score < 8:
        feedback_parts.append("📊 MISSING METRICS:")
        feedback_parts.append("• No quantifiable results mentioned. Big tech LOVES numbers.")
        feedback_parts.append("• Add metrics like: '20% improvement', 'reduced from 2 weeks to 3 days', '$50K saved'.")
        feedback_parts.append("")
    
    # Overall verdict - Be honest like a real interviewer
    feedback_parts.append("📝 OVERALL ASSESSMENT:")
    if avg_score >= 8:
        feedback_parts.append("• STRONG RESPONSE - Would likely receive a 'Strong Hire' signal for behavioral fit.")
        feedback_parts.append("• This demonstrates the depth and structure expected at top tech companies.")
    elif avg_score >= 6:
        feedback_parts.append("• ACCEPTABLE RESPONSE - 'Inclined' but not exceptional.")
        feedback_parts.append("• In a competitive loop, this might not be enough. Aim higher.")
    elif avg_score >= 4:
        feedback_parts.append("• WEAK RESPONSE - Would likely receive a 'Not Inclined' rating.")
        feedback_parts.append("• At companies like Amazon (Bar Raiser interviews), this would be concerning.")
        feedback_parts.append("• You need significant improvement in structure and specificity.")
    elif avg_score >= 2:
        feedback_parts.append("• POOR RESPONSE - Would result in 'Strong No Hire' feedback.")
        feedback_parts.append("• This answer shows lack of preparation for behavioral interviews.")
        feedback_parts.append("• Recommend: Study STAR method, prepare 6-8 stories with specific metrics.")
    else:
        feedback_parts.append("• UNACCEPTABLE RESPONSE - Interview would likely be stopped early.")
        feedback_parts.append("• This type of answer suggests either unprepared candidate or poor fit.")
        feedback_parts.append("• Action required: Complete preparation overhaul before real interviews.")
    
    return "\n".join(feedback_parts)


def get_hr_question_bank() -> List[Dict]:
    """Return common HR behavioral questions."""
    return [
        {
            "question": "Tell me about a time you faced a significant challenge at work.",
            "focus": ["problem-solving", "resilience", "action-oriented"]
        },
        {
            "question": "Describe a situation where you had to work with a difficult team member.",
            "focus": ["teamwork", "conflict resolution", "communication"]
        },
        {
            "question": "Give an example of a time you showed leadership.",
            "focus": ["leadership", "initiative", "influence"]
        },
        {
            "question": "Tell me about a time you failed and what you learned from it.",
            "focus": ["self-awareness", "growth mindset", "accountability"]
        },
        {
            "question": "Describe a situation where you had to meet a tight deadline.",
            "focus": ["time management", "prioritization", "pressure handling"]
        },
        {
            "question": "Tell me about a time you went above and beyond for a project.",
            "focus": ["initiative", "dedication", "impact"]
        },
        {
            "question": "Describe a situation where you had to persuade others to see your point of view.",
            "focus": ["communication", "influence", "negotiation"]
        },
        {
            "question": "Tell me about a time you received critical feedback.",
            "focus": ["receptiveness", "self-improvement", "professionalism"]
        }
    ]
