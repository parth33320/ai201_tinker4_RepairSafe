def classify_safety_tier(question: str) -> str:
    """
    STUB: Classifies the safety tier of a repair question.
    In a real implementation, this would use an LLM or ruleset.
    """
    # For testing purposes, we can use keywords or simple logic
    q = question.lower()
    if "electrical" in q or "gas" in q or "structural" in q or "permit" in q:
        return "refuse"
    elif "leak" in q or "heavy" in q or "ladder" in q:
        return "caution"
    else:
        return "safe"
