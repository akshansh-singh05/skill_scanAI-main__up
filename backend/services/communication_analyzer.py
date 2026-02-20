"""
Communication Analyzer Service

Analyzes text-based responses for communication quality:
- Filler words detection
- Answer length analysis  
- Structure detection (STAR method, clear sections)
- Clarity scoring
- Confidence indicators
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


# Filler words and phrases to detect
FILLER_WORDS = {
    "um", "uh", "like", "you know", "basically", "actually", "literally",
    "so", "well", "i mean", "kind of", "sort of", "i guess", "i think",
    "right", "okay", "er", "ah", "hmm", "yeah", "yep", "nope",
    "stuff", "things", "whatever", "anyway", "anyways", "honestly",
    "obviously", "clearly", "definitely", "absolutely", "totally",
    "just", "really", "very", "pretty much", "i feel like",
    "to be honest", "tbh", "at the end of the day", "going forward",
    "in terms of", "with respect to", "as such", "per se",
}

# Weak phrases that reduce impact
WEAK_PHRASES = {
    "i tried to": "I accomplished",
    "i helped with": "I led/contributed to",
    "i was responsible for": "I managed/delivered",
    "we did": "I specifically contributed",
    "it was good": "quantify the impact",
    "it went well": "describe specific outcomes",
    "i think i": "I confidently",
    "maybe i could": "I will",
    "i'm not sure but": "Based on my analysis",
}

# Structure indicators (STAR method)
STRUCTURE_KEYWORDS = {
    "situation": ["situation", "context", "background", "scenario", "when", "while working"],
    "task": ["task", "goal", "objective", "challenge", "problem", "needed to", "had to", "responsible for"],
    "action": ["action", "i did", "i implemented", "i created", "i developed", "i led", "i designed", "steps i took"],
    "result": ["result", "outcome", "impact", "achieved", "improved", "increased", "decreased", "saved", "delivered", "success"],
}

# Clarity indicators
CLARITY_POSITIVE = [
    "specifically", "for example", "such as", "in particular",
    "the reason", "because", "therefore", "as a result",
    "first", "second", "third", "finally", "in conclusion",
    "my approach", "i decided to", "the key insight",
]

CLARITY_NEGATIVE = [
    "etc", "and so on", "things like that", "you get the idea",
    "blah blah", "yada yada", "something something",
    "long story short", "to make a long story short",
]


def analyze_communication(text: str, is_behavioral: bool = False) -> Dict:
    """
    Analyze communication quality of a response.
    
    Args:
        text: The response text to analyze
        is_behavioral: Whether this is a behavioral question (stricter structure check)
        
    Returns:
        Comprehensive analysis with scores and feedback
    """
    if not text or len(text.strip()) < 10:
        return {
            "overall_score": 0,
            "clarity_score": 0,
            "structure_score": 0,
            "confidence_score": 0,
            "issues": ["Response is too short to analyze"],
            "suggestions": ["Provide a more detailed response"],
            "filler_words": [],
            "word_count": 0,
        }
    
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Analyze different aspects
    filler_analysis = _analyze_fillers(text_lower, words)
    length_analysis = _analyze_length(word_count, sentence_count, is_behavioral)
    structure_analysis = _analyze_structure(text_lower, is_behavioral)
    clarity_analysis = _analyze_clarity(text_lower, sentences)
    confidence_analysis = _analyze_confidence(text_lower)
    
    # Calculate scores (0-10 scale)
    clarity_score = _calculate_clarity_score(
        filler_analysis, length_analysis, clarity_analysis
    )
    structure_score = _calculate_structure_score(
        structure_analysis, length_analysis, is_behavioral
    )
    confidence_score = _calculate_confidence_score(
        confidence_analysis, filler_analysis
    )
    
    # Overall score (weighted average)
    overall_score = int(
        clarity_score * 0.35 +
        structure_score * 0.35 +
        confidence_score * 0.30
    )
    
    # Compile issues and suggestions
    issues = _compile_issues(filler_analysis, length_analysis, structure_analysis, clarity_analysis)
    suggestions = _generate_suggestions(filler_analysis, length_analysis, structure_analysis, clarity_analysis, confidence_analysis)
    
    return {
        "overall_score": overall_score,
        "clarity_score": clarity_score,
        "structure_score": structure_score,
        "confidence_score": confidence_score,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "filler_words": filler_analysis["found"],
        "filler_count": filler_analysis["count"],
        "weak_phrases": filler_analysis["weak_phrases"],
        "structure_detected": structure_analysis["elements_found"],
        "issues": issues[:5],  # Top 5 issues
        "suggestions": suggestions[:4],  # Top 4 suggestions
        "strengths": _identify_strengths(clarity_score, structure_score, confidence_score, structure_analysis),
        "detailed_breakdown": {
            "filler_percentage": round(filler_analysis["percentage"], 1),
            "avg_sentence_length": round(word_count / max(sentence_count, 1), 1),
            "structure_completeness": structure_analysis["completeness"],
            "has_specific_examples": clarity_analysis["has_examples"],
            "has_quantified_results": structure_analysis["has_metrics"],
        }
    }


def _analyze_fillers(text_lower: str, words: List[str]) -> Dict:
    """Detect filler words and weak phrases."""
    found_fillers = []
    filler_count = 0
    
    # Check single-word fillers
    word_counter = Counter(words)
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word in FILLER_WORDS:
            count = word_counter.get(word, 0)
            if clean_word not in [f["word"] for f in found_fillers]:
                found_fillers.append({"word": clean_word, "count": count})
                filler_count += count
    
    # Check multi-word fillers
    for filler in FILLER_WORDS:
        if ' ' in filler and filler in text_lower:
            count = text_lower.count(filler)
            found_fillers.append({"word": filler, "count": count})
            filler_count += count
    
    # Check weak phrases
    weak_found = []
    for weak, better in WEAK_PHRASES.items():
        if weak in text_lower:
            weak_found.append({"phrase": weak, "suggestion": better})
    
    total_words = len(words)
    percentage = (filler_count / total_words * 100) if total_words > 0 else 0
    
    return {
        "found": found_fillers,
        "count": filler_count,
        "percentage": percentage,
        "weak_phrases": weak_found,
    }


def _analyze_length(word_count: int, sentence_count: int, is_behavioral: bool) -> Dict:
    """Analyze response length appropriateness."""
    # Ideal ranges
    if is_behavioral:
        ideal_min, ideal_max = 100, 300  # STAR responses should be detailed
    else:
        ideal_min, ideal_max = 50, 200  # Technical can be more concise
    
    if word_count < 20:
        status = "too_short"
        feedback = "Response is too brief. Elaborate with more details."
    elif word_count < ideal_min:
        status = "short"
        feedback = "Consider adding more context or examples."
    elif word_count > ideal_max * 1.5:
        status = "too_long"
        feedback = "Response is lengthy. Focus on key points."
    elif word_count > ideal_max:
        status = "long"
        feedback = "Good detail, but could be more concise."
    else:
        status = "ideal"
        feedback = "Good response length."
    
    avg_sentence_length = word_count / max(sentence_count, 1)
    
    return {
        "word_count": word_count,
        "status": status,
        "feedback": feedback,
        "avg_sentence_length": avg_sentence_length,
        "sentence_variety": "good" if 10 < avg_sentence_length < 25 else "needs_work",
    }


def _analyze_structure(text_lower: str, is_behavioral: bool) -> Dict:
    """Analyze response structure (STAR method for behavioral)."""
    elements_found = []
    
    for element, keywords in STRUCTURE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                if element not in elements_found:
                    elements_found.append(element)
                break
    
    completeness = len(elements_found) / 4 * 100  # 4 STAR elements
    
    # Check for metrics/quantification
    has_metrics = bool(re.search(r'\d+%|\d+\s*(percent|users|customers|times|x|hours|days|weeks|months)', text_lower))
    
    # Check for transition words
    transitions = ["first", "then", "next", "finally", "as a result", "because", "therefore", "however"]
    has_transitions = any(t in text_lower for t in transitions)
    
    return {
        "elements_found": elements_found,
        "completeness": completeness,
        "has_metrics": has_metrics,
        "has_transitions": has_transitions,
        "missing_elements": [e for e in ["situation", "task", "action", "result"] if e not in elements_found],
    }


def _analyze_clarity(text_lower: str, sentences: List[str]) -> Dict:
    """Analyze response clarity."""
    # Check for specific examples
    example_indicators = ["for example", "for instance", "such as", "specifically", "in particular"]
    has_examples = any(ind in text_lower for ind in example_indicators)
    
    # Check for clarity indicators
    positive_count = sum(1 for p in CLARITY_POSITIVE if p in text_lower)
    negative_count = sum(1 for n in CLARITY_NEGATIVE if n in text_lower)
    
    # Check for vague language
    vague_terms = ["something", "somehow", "somewhere", "stuff", "things", "whatever", "etc"]
    vague_count = sum(1 for v in vague_terms if v in text_lower)
    
    # Sentence variety (not all same length)
    sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
    if sentence_lengths:
        variance = max(sentence_lengths) - min(sentence_lengths) if len(sentence_lengths) > 1 else 0
        has_variety = variance > 5
    else:
        has_variety = False
    
    return {
        "has_examples": has_examples,
        "positive_indicators": positive_count,
        "negative_indicators": negative_count,
        "vague_count": vague_count,
        "has_sentence_variety": has_variety,
    }


def _analyze_confidence(text_lower: str) -> Dict:
    """Analyze confidence level in response."""
    # Confident language
    confident = ["i achieved", "i delivered", "i led", "i created", "i solved", "i implemented", "successfully", "effectively"]
    confident_count = sum(1 for c in confident if c in text_lower)
    
    # Uncertain language
    uncertain = ["i think", "i guess", "maybe", "probably", "i'm not sure", "kind of", "sort of", "i tried"]
    uncertain_count = sum(1 for u in uncertain if u in text_lower)
    
    # Passive vs active voice indicators
    passive_indicators = ["was done", "was made", "was created", "were developed", "has been"]
    passive_count = sum(1 for p in passive_indicators if p in text_lower)
    
    return {
        "confident_count": confident_count,
        "uncertain_count": uncertain_count,
        "passive_count": passive_count,
        "uses_active_voice": passive_count < 2,
    }


def _calculate_clarity_score(filler: Dict, length: Dict, clarity: Dict) -> int:
    """Calculate clarity score (0-10)."""
    score = 7  # Base score
    
    # Filler word penalty
    if filler["percentage"] > 10:
        score -= 3
    elif filler["percentage"] > 5:
        score -= 2
    elif filler["percentage"] > 2:
        score -= 1
    
    # Length adjustments
    if length["status"] == "too_short":
        score -= 3
    elif length["status"] == "short":
        score -= 1
    elif length["status"] == "too_long":
        score -= 1
    
    # Clarity bonuses/penalties
    score += min(clarity["positive_indicators"], 2)
    score -= min(clarity["negative_indicators"], 2)
    score -= min(clarity["vague_count"], 2)
    
    if clarity["has_examples"]:
        score += 1
    
    return max(0, min(10, score))


def _calculate_structure_score(structure: Dict, length: Dict, is_behavioral: bool) -> int:
    """Calculate structure score (0-10)."""
    if is_behavioral:
        # STAR method scoring
        base_score = int(structure["completeness"] / 10)  # 0-10 based on completeness
    else:
        base_score = 6  # Technical questions have looser structure requirements
        if structure["has_transitions"]:
            base_score += 1
    
    # Bonus for metrics
    if structure["has_metrics"]:
        base_score += 1
    
    # Bonus for transitions
    if structure["has_transitions"]:
        base_score += 1
    
    # Length penalty for structure
    if length["status"] == "too_short":
        base_score -= 2
    
    return max(0, min(10, base_score))


def _calculate_confidence_score(confidence: Dict, filler: Dict) -> int:
    """Calculate confidence score (0-10)."""
    score = 6  # Base score
    
    score += min(confidence["confident_count"], 3)
    score -= min(confidence["uncertain_count"], 3)
    score -= min(confidence["passive_count"], 2)
    
    # Filler words reduce perceived confidence
    if filler["percentage"] > 5:
        score -= 1
    
    if confidence["uses_active_voice"]:
        score += 1
    
    return max(0, min(10, score))


def _compile_issues(filler: Dict, length: Dict, structure: Dict, clarity: Dict) -> List[str]:
    """Compile list of issues found."""
    issues = []
    
    if filler["count"] > 3:
        issues.append(f"High filler word usage ({filler['count']} instances)")
    
    if filler["weak_phrases"]:
        issues.append(f"Weak phrases detected: '{filler['weak_phrases'][0]['phrase']}'")
    
    if length["status"] == "too_short":
        issues.append("Response is too brief and lacks detail")
    elif length["status"] == "too_long":
        issues.append("Response is overly long - consider being more concise")
    
    if structure["missing_elements"]:
        missing = ", ".join(structure["missing_elements"][:2])
        issues.append(f"Missing STAR elements: {missing}")
    
    if not structure["has_metrics"]:
        issues.append("No quantified results or metrics provided")
    
    if clarity["vague_count"] > 2:
        issues.append("Too much vague language used")
    
    if not clarity["has_examples"]:
        issues.append("No specific examples provided")
    
    return issues


def _generate_suggestions(filler: Dict, length: Dict, structure: Dict, clarity: Dict, confidence: Dict) -> List[str]:
    """Generate actionable suggestions."""
    suggestions = []
    
    if filler["weak_phrases"]:
        wp = filler["weak_phrases"][0]
        suggestions.append(f"Replace '{wp['phrase']}' with stronger language: {wp['suggestion']}")
    
    if filler["found"]:
        top_filler = max(filler["found"], key=lambda x: x["count"])
        suggestions.append(f"Reduce usage of '{top_filler['word']}' (used {top_filler['count']} times)")
    
    if not structure["has_metrics"]:
        suggestions.append("Add specific numbers: percentages, time saved, users impacted, etc.")
    
    if structure["missing_elements"]:
        if "result" in structure["missing_elements"]:
            suggestions.append("End with clear results - what was the measurable outcome?")
        if "situation" in structure["missing_elements"]:
            suggestions.append("Start by setting the context - when and where did this happen?")
    
    if not clarity["has_examples"]:
        suggestions.append("Include a specific example using 'for example' or 'specifically'")
    
    if confidence["uncertain_count"] > confidence["confident_count"]:
        suggestions.append("Use more confident language: 'I achieved' instead of 'I tried'")
    
    if not confidence["uses_active_voice"]:
        suggestions.append("Use active voice: 'I created' instead of 'was created'")
    
    return suggestions


def _identify_strengths(clarity: int, structure: int, confidence: int, structure_analysis: Dict) -> List[str]:
    """Identify strengths in the response."""
    strengths = []
    
    if clarity >= 7:
        strengths.append("Clear and articulate communication")
    
    if structure >= 7:
        strengths.append("Well-structured response")
    
    if confidence >= 7:
        strengths.append("Confident and assertive tone")
    
    if structure_analysis["has_metrics"]:
        strengths.append("Good use of quantified results")
    
    if structure_analysis["completeness"] >= 75:
        strengths.append("Complete STAR format")
    
    if not strengths:
        strengths.append("Room for improvement in communication style")
    
    return strengths[:3]


def get_communication_grade(score: int) -> Dict:
    """Convert score to letter grade with description."""
    if score >= 9:
        return {"grade": "A+", "label": "Excellent", "color": "green"}
    elif score >= 8:
        return {"grade": "A", "label": "Great", "color": "green"}
    elif score >= 7:
        return {"grade": "B+", "label": "Good", "color": "blue"}
    elif score >= 6:
        return {"grade": "B", "label": "Satisfactory", "color": "blue"}
    elif score >= 5:
        return {"grade": "C+", "label": "Needs Work", "color": "yellow"}
    elif score >= 4:
        return {"grade": "C", "label": "Below Average", "color": "yellow"}
    else:
        return {"grade": "D", "label": "Poor", "color": "red"}
