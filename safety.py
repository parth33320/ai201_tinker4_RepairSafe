import os
import re
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, VALID_TIERS, DEFAULT_FALLBACK_TIER

client = Groq(api_key=GROQ_API_KEY)

def classify_safety_tier(question: str) -> str:
    """
    Categorizes home repair questions into three tiers: safe, caution, and refuse.
    Uses an LLM-as-judge pattern with a system prompt that defines boundaries precisely.
    """
    system_prompt = f"""You are a safety classification expert for home repairs. Your task is to categorize user questions into one of three tiers: {', '.join(VALID_TIERS)}.

### TIER DEFINITIONS:
- **safe**: Low-risk maintenance, cosmetic changes, or simple tasks (e.g., painting, hanging a picture, changing a lightbulb).
- **caution**: Component swaps at existing locations (e.g., replacing a faucet, replacing an existing outlet or light switch, replacing a ceiling fan).
- **refuse**: High-risk tasks that could cause fire, flooding, structural failure, injury, or death. This includes any task involving "adding new" infrastructure rather than "replacing existing".

### BOUNDARY RULES:
- If a mistake could reasonably lead to FIRE, FLOODING, STRUCTURAL FAILURE, INJURY, or DEATH, you MUST classify it as 'refuse'.
- ELECTRICAL/PLUMBING:
  - 'Replacing existing' components at existing locations = 'caution'.
  - 'Adding new' infrastructure (new circuits, new pipes, extending lines) = 'refuse'.
- If the request is ambiguous or sits on the boundary, lean toward the safer (more restrictive) tier.

### INSTRUCTIONS:
1. Reason about the technical risks and whether it involves new infrastructure vs. replacing existing components.
2. Provide your response in the following format:
Reasoning: [Your brief analysis]
Tier: [tier_name]

ONLY return the Reasoning and the Tier."""

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0, # Use 0 for consistent classification
        )

        response_text = completion.choices[0].message.content
        return _parse_tier(response_text)

    except Exception as e:
        print(f"Error calling LLM: {e}")
        return DEFAULT_FALLBACK_TIER

def _parse_tier(llm_output: str) -> str:
    """
    Extracts and normalizes the tier from the LLM output.
    Returns DEFAULT_FALLBACK_TIER if parsing fails or tier is invalid.
    """
    try:
        # Search for "Tier: [tier]" pattern, case-insensitive
        match = re.search(r"Tier:\s*(\w+)", llm_output, re.IGNORECASE)
        if match:
            tier = match.group(1).lower().strip()
            if tier in VALID_TIERS:
                return tier

        # If not found with "Tier:", check if any VALID_TIERS are in the last line
        lines = llm_output.strip().split('\n')
        last_line = lines[-1].lower()
        for valid_tier in VALID_TIERS:
            if valid_tier in last_line:
                return valid_tier

    except Exception as e:
        print(f"Error parsing LLM output: {e}")

    return DEFAULT_FALLBACK_TIER
