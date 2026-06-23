import os
from groq import Groq
from dotenv import load_dotenv
import config

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_safety_tier(question):
    """
    You are a safety classifier for a home repair assistant. Your task is to categorize user questions into one of three tiers: safe, caution, refuse.

    ### TIER DEFINITIONS:
    - **safe**: Routine DIY repairs. Low risk, easy to fix if a mistake is made. (e.g., painting, patching small holes, replacing cabinet hardware).
    - **caution**: Moderate risk repairs. Doable for a motivated DIYer, but mistakes have a cost (e.g., leaky pipes, replacing existing fixtures).
    - **refuse**: High-risk repairs. Mistakes can lead to catastrophic failure. REQUIRES A PROFESSIONAL.

    ### MANDATORY DECISION RULES:
    1. **The "Catastrophe" Rule**: If an amateur mistake could cause FIRE, FLOODING, STRUCTURAL FAILURE, INJURY, or DEATH, you MUST return "refuse".
    2. **The Electrical Rule**:
        - "Replacing existing" components (like an outlet, switch, or light fixture) is **caution**.
        - "Adding new" infrastructure (like running new wire, adding a new outlet, or opening the electrical panel) is **refuse**.
    3. **Framing doesn't change the tier**: If a user asks to "just move a switch six inches", that requires new wiring and is **refuse**, regardless of how simple the user makes it sound.

    ### OUTPUT FORMAT:
    Return only the tier name in lowercase. No explanation.
    Example Output: safe
    """
    try:
        # Use the prompt defined in the docstring as the system message
        system_prompt = classify_safety_tier.__doc__

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model=config.GROQ_MODEL,
            temperature=0, # Temperature 0 is best for structured classification
        )
        
        # Normalization and strict equality check
        raw_output = response.choices[0].message.content
        # Normalization handles common LLM formatting variations like capitalized letters,
        # surrounding quotes, or trailing punctuation.
        normalized_tier = raw_output.strip(' \t\n\r.?!,"\'').lower()
        
        if normalized_tier in config.VALID_TIERS:
            return normalized_tier
        return config.DEFAULT_FALLBACK_TIER
    except Exception:
        # Safety fallback for API errors or unexpected model behavior
        return config.DEFAULT_FALLBACK_TIER
