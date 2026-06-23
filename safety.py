import os
from groq import Groq
from dotenv import load_dotenv
import config

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_safety_tier(question):
    """
    Classifies a home repair question into one of the VALID_TIERS using an LLM.
    
    Decision Rule:
    - If an amateur mistake could cause fire, flooding, structural failure, injury, or death -> refuse.
    - Electrical: "replacing existing" (caution) vs "adding new" (refuse).
    - If unparseable or invalid -> refuse.
    """
    
    system_prompt = f"""
You are a safety classifier for a home repair assistant. Your task is to categorize user questions into one of three tiers: {", ".join(config.VALID_TIERS)}.

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
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            model=config.GROQ_MODEL,
            temperature=0,
        )
        
        raw_output = chat_completion.choices[0].message.content.strip().lower()
        
        # Basic parsing to handle cases where the LLM might include extra words
        for tier in config.VALID_TIERS:
            if tier in raw_output:
                return tier
        
        return config.DEFAULT_FALLBACK_TIER
        
    except Exception as e:
        print(f"Error in classification: {e}")
        return config.DEFAULT_FALLBACK_TIER
