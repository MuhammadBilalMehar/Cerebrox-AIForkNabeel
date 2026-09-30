NOTES_SYSTEM_PROMPT = (
    "You are an educational content writer for CerebroX AI, a learning platform. "
    "Always respond with a single JSON object with exactly these keys: "
    "introduction, explanation, key_terms (list of strings), examples (list of strings), "
    "important_points (list of strings), summary."
)

def notes_user_prompt(course: str, topic: str, study_level: str, length: str) -> str:
    return (
        f"Write study notes for the topic '{topic}' in the course '{course}'. "
        f"The student's study level is: {study_level} — pitch the vocabulary, depth, and "
        f"assumed background knowledge appropriately for that level. Length: {length}. "
        "Keep it accurate, clear, and structured for a student revising for a quiz."
    )


MCQ_SYSTEM_PROMPT = (
    "You are a quiz question generator for CerebroX AI. "
    "Always respond with a single JSON object: {\"questions\": [...]}. "
    "Each item must have: question, option_a, option_b, option_c, option_d, "
    "correct_answer (one of 'A','B','C','D'), explanation."
)

def mcq_user_prompt(course: str, topic: str, study_level: str, difficulty: str, count: int) -> str:
    return (
        f"Generate {count} multiple-choice questions about '{topic}' from the course '{course}'. "
        f"The student's study level is: {study_level}. Difficulty: {difficulty}. "
        "Exactly four options each, only one correct answer, and a one-sentence explanation. "
        "Calibrate vocabulary and concept depth to the student's study level."
    )


RECOMMENDATION_SYSTEM_PROMPT = (
    "You are a supportive academic advisor for CerebroX AI. "
    "Respond with a single JSON object: {\"message\": \"...\"} containing one short, "
    "encouraging, actionable paragraph (2-3 sentences)."
)

def recommendation_user_prompt(topic: str, score_percent: float, status: str) -> str:
    return (
        f"A student scored {score_percent:.0f}% on '{topic}', classified as '{status}'. "
        "Write a short personalized recommendation for what they should do next."
    )
