from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re

router = APIRouter()


class VideoAnalysisRequest(BaseModel):
    transcript: str
    question: Optional[str] = None
    duration: Optional[int] = 60


class VideoAnalysisResponse(BaseModel):
    confidence_score: float
    clarity_score: float
    filler_words_count: int
    filler_words_found: List[str]
    sentiment: str
    feedback: str
    suggestions: List[str]
    word_count: int
    speaking_pace: str


# Common filler words to detect
FILLER_WORDS = [
    'um', 'uh', 'like', 'you know', 'so', 'basically', 'actually', 'literally',
    'i mean', 'kind of', 'sort of', 'right', 'okay', 'well', 'just', 'really',
    'very', 'honestly', 'frankly', 'essentially', 'definitely', 'totally',
    'absolutely', 'obviously', 'clearly', 'anyway', 'anyways', 'whatever'
]

# Positive words for sentiment analysis
POSITIVE_WORDS = [
    'passionate', 'excited', 'love', 'enjoy', 'excellent', 'great', 'amazing',
    'wonderful', 'fantastic', 'successful', 'achieved', 'accomplished', 'proud',
    'confident', 'motivated', 'dedicated', 'enthusiastic', 'committed', 'skilled',
    'experienced', 'innovative', 'creative', 'leader', 'team', 'collaboration',
    'growth', 'opportunity', 'challenge', 'solution', 'improve', 'develop'
]

# Negative words for sentiment analysis
NEGATIVE_WORDS = [
    'hate', 'dislike', 'terrible', 'awful', 'bad', 'poor', 'weak', 'failed',
    'struggle', 'difficult', 'problem', 'issue', 'worried', 'nervous', 'anxious',
    'scared', 'afraid', 'unsure', 'confused', 'frustrated', 'stressed'
]

# Confident language patterns
CONFIDENT_PATTERNS = [
    r'\bi achieved\b', r'\bi led\b', r'\bi managed\b', r'\bi created\b',
    r'\bi developed\b', r'\bi implemented\b', r'\bi designed\b', r'\bi built\b',
    r'\bmy experience\b', r'\bmy skills\b', r'\bi am confident\b', r'\bi believe\b',
    r'\bi can\b', r'\bi will\b', r'\bi have\b'
]

# Uncertain language patterns
UNCERTAIN_PATTERNS = [
    r'\bi think maybe\b', r'\bi guess\b', r'\bi\'m not sure\b', r'\bperhaps\b',
    r'\bmaybe\b', r'\bprobably\b', r'\bkind of\b', r'\bsort of\b', r'\bi don\'t know\b'
]


def count_filler_words(text: str) -> tuple:
    """Count filler words in the transcript."""
    text_lower = text.lower()
    found_fillers = []
    count = 0
    
    for filler in FILLER_WORDS:
        # Count occurrences of each filler word
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            count += len(matches)
            found_fillers.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_fillers = []
    for filler in found_fillers:
        if filler not in seen:
            seen.add(filler)
            unique_fillers.append(filler)
    
    return count, unique_fillers


def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of the transcript."""
    text_lower = text.lower()
    
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    # Check for confident patterns
    confident_count = sum(1 for pattern in CONFIDENT_PATTERNS if re.search(pattern, text_lower))
    uncertain_count = sum(1 for pattern in UNCERTAIN_PATTERNS if re.search(pattern, text_lower))
    
    if confident_count > uncertain_count + 2:
        return 'confident'
    elif uncertain_count > confident_count + 1:
        return 'nervous'
    elif positive_count > negative_count + 2:
        return 'positive'
    elif negative_count > positive_count + 1:
        return 'negative'
    else:
        return 'neutral'


def calculate_confidence_score(text: str, filler_count: int, word_count: int) -> float:
    """Calculate confidence score based on various factors."""
    if word_count == 0:
        return 0.0
    
    text_lower = text.lower()
    
    # Base score
    score = 5.0
    
    # Deduct for filler words (more fillers = less confident)
    filler_ratio = filler_count / max(word_count, 1)
    score -= min(filler_ratio * 20, 3)  # Max deduction of 3
    
    # Add points for confident language
    confident_count = sum(1 for pattern in CONFIDENT_PATTERNS if re.search(pattern, text_lower))
    score += min(confident_count * 0.5, 2)  # Max addition of 2
    
    # Deduct for uncertain language
    uncertain_count = sum(1 for pattern in UNCERTAIN_PATTERNS if re.search(pattern, text_lower))
    score -= min(uncertain_count * 0.5, 2)  # Max deduction of 2
    
    # Add points for good word count (not too short)
    if word_count >= 100:
        score += 1
    elif word_count >= 50:
        score += 0.5
    
    # Add points for structured response (contains transition words)
    structure_words = ['first', 'second', 'third', 'finally', 'additionally', 'moreover', 'however', 'therefore', 'consequently', 'in conclusion']
    structure_count = sum(1 for word in structure_words if word in text_lower)
    score += min(structure_count * 0.3, 1)
    
    return max(0, min(10, round(score, 1)))


def calculate_clarity_score(text: str, word_count: int, duration: int) -> float:
    """Calculate clarity score based on sentence structure and pace."""
    if word_count == 0:
        return 0.0
    
    # Base score
    score = 5.0
    
    # Count sentences
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Average words per sentence (ideal: 15-25)
    if sentence_count > 0:
        avg_words_per_sentence = word_count / sentence_count
        if 15 <= avg_words_per_sentence <= 25:
            score += 1.5
        elif 10 <= avg_words_per_sentence <= 30:
            score += 0.5
        else:
            score -= 1
    
    # Speaking pace (words per minute, ideal: 120-150)
    if duration > 0:
        wpm = (word_count / duration) * 60
        if 120 <= wpm <= 150:
            score += 1.5
        elif 100 <= wpm <= 170:
            score += 0.5
        elif wpm < 80 or wpm > 200:
            score -= 1
    
    # Check for complete sentences (starts with capital, ends with punctuation)
    complete_sentences = len(re.findall(r'[A-Z][^.!?]*[.!?]', text))
    if complete_sentences >= 3:
        score += 1
    
    # Vocabulary variety (unique words / total words)
    words = text.lower().split()
    unique_words = set(words)
    if len(words) > 0:
        variety_ratio = len(unique_words) / len(words)
        if variety_ratio >= 0.7:
            score += 1
        elif variety_ratio >= 0.5:
            score += 0.5
    
    return max(0, min(10, round(score, 1)))


def get_speaking_pace(word_count: int, duration: int) -> str:
    """Determine speaking pace category."""
    if duration == 0:
        return 'unknown'
    
    wpm = (word_count / duration) * 60
    
    if wpm < 100:
        return 'slow'
    elif wpm < 130:
        return 'moderate'
    elif wpm < 160:
        return 'good'
    elif wpm < 200:
        return 'fast'
    else:
        return 'very fast'


def generate_feedback(
    confidence_score: float,
    clarity_score: float,
    filler_count: int,
    sentiment: str,
    word_count: int,
    speaking_pace: str
) -> str:
    """Generate personalized feedback based on analysis."""
    feedback_parts = []
    
    # Overall assessment
    avg_score = (confidence_score + clarity_score) / 2
    if avg_score >= 8:
        feedback_parts.append("Excellent response! You demonstrated strong communication skills.")
    elif avg_score >= 6:
        feedback_parts.append("Good effort! Your response shows promise with some areas for improvement.")
    elif avg_score >= 4:
        feedback_parts.append("Decent attempt. There are several areas you can work on to improve.")
    else:
        feedback_parts.append("Keep practicing! Focus on the suggestions below to improve your interview skills.")
    
    # Confidence feedback
    if confidence_score >= 7:
        feedback_parts.append("You spoke with confidence and used assertive language.")
    elif confidence_score >= 5:
        feedback_parts.append("Your confidence level was moderate. Try using more assertive language.")
    else:
        feedback_parts.append("Work on projecting more confidence by using 'I achieved' instead of 'I think I might have'.")
    
    # Filler words feedback
    if filler_count == 0:
        feedback_parts.append("Great job avoiding filler words!")
    elif filler_count <= 3:
        feedback_parts.append(f"You used {filler_count} filler word(s), which is acceptable.")
    else:
        feedback_parts.append(f"Try to reduce filler words (you used {filler_count}). Practice pausing instead of saying 'um' or 'like'.")
    
    # Speaking pace feedback
    if speaking_pace == 'good':
        feedback_parts.append("Your speaking pace was ideal for clear communication.")
    elif speaking_pace == 'slow':
        feedback_parts.append("Consider speaking a bit faster to maintain engagement.")
    elif speaking_pace in ['fast', 'very fast']:
        feedback_parts.append("Try to slow down slightly to ensure clarity.")
    
    return " ".join(feedback_parts)


def generate_suggestions(
    confidence_score: float,
    clarity_score: float,
    filler_count: int,
    word_count: int,
    sentiment: str
) -> List[str]:
    """Generate specific improvement suggestions."""
    suggestions = []
    
    if confidence_score < 7:
        suggestions.append("Use action verbs like 'achieved', 'led', 'created' to sound more confident.")
    
    if filler_count > 3:
        suggestions.append("Practice pausing silently instead of using filler words like 'um' or 'like'.")
    
    if clarity_score < 7:
        suggestions.append("Structure your response with clear beginning, middle, and end.")
    
    if word_count < 50:
        suggestions.append("Elaborate more on your answers. Use the STAR method (Situation, Task, Action, Result).")
    
    if sentiment == 'nervous':
        suggestions.append("Take a deep breath before answering. Remember, it's a conversation, not an interrogation.")
    
    if sentiment == 'negative':
        suggestions.append("Try to frame challenges positively. Focus on what you learned rather than difficulties.")
    
    if confidence_score >= 7 and clarity_score >= 7 and filler_count <= 3:
        suggestions.append("Keep up the great work! Consider adding specific metrics or examples to make your answers even stronger.")
    
    # Always provide at least one suggestion
    if not suggestions:
        suggestions.append("Continue practicing regularly to maintain and improve your interview skills.")
    
    return suggestions[:5]  # Limit to 5 suggestions


@router.post("/video-analysis", response_model=VideoAnalysisResponse)
async def analyze_video_transcript(request: VideoAnalysisRequest):
    """
    Analyze a video interview transcript and provide scores and feedback.
    """
    transcript = request.transcript.strip()
    duration = request.duration or 60
    
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")
    
    # Calculate metrics
    word_count = len(transcript.split())
    filler_count, filler_words_found = count_filler_words(transcript)
    sentiment = analyze_sentiment(transcript)
    speaking_pace = get_speaking_pace(word_count, duration)
    
    confidence_score = calculate_confidence_score(transcript, filler_count, word_count)
    clarity_score = calculate_clarity_score(transcript, word_count, duration)
    
    feedback = generate_feedback(
        confidence_score, clarity_score, filler_count, 
        sentiment, word_count, speaking_pace
    )
    suggestions = generate_suggestions(
        confidence_score, clarity_score, filler_count, 
        word_count, sentiment
    )
    
    return VideoAnalysisResponse(
        confidence_score=confidence_score,
        clarity_score=clarity_score,
        filler_words_count=filler_count,
        filler_words_found=filler_words_found,
        sentiment=sentiment,
        feedback=feedback,
        suggestions=suggestions,
        word_count=word_count,
        speaking_pace=speaking_pace
    )
