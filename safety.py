import os
from groq import Groq
from dotenv import load_dotenv
import config

load_dotenv()

# The Groq client is initialized using your API key from the .env file [5].
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_safety_tier(question):
    """
    You are a safety classifier for a home repair assistant. 
    Your task is to categorize user questions into one of three tiers: safe, caution, refuse. [5]
    """
    
    # System prompt built using precise definitions from the classifier spec [3, 4].
    # It incorporates the critical fire/flood/death rule and the electrical "replace vs. add" distinction [6, 7].
    system_prompt = f"""
    You are a safety classifier for home repair questions. Categorize the user's question into exactly one of these tiers:
    
    - safe: Routine DIY tasks with minimal risk and high recoverability (e.g., painting, basic patching).
    - caution: Doable but risky tasks where errors cause manageable damage (e.g., component swaps like replacing an existing outlet).
    - refuse: High-stakes tasks where mistakes lead to fire, flooding, structural failure, injury, or death (e.g., new electrical/plumbing infrastructure).
    
    DECISION RULE: If an amateur mistake could cause fire, flooding, structural failure, injury, or death, you MUST classify as 'refuse'. [4, 6]
    ELECTRICAL RULE: 'Replacing existing' components at an existing location is 'caution'. 'Adding new' electrical infrastructure (new wire, new circuits, opening the panel) is 'refuse'. [7, 8]
    
    Return your response in this exact format:
    Tier: <tier>
    Reason: <brief explanation>
    """

    try:
        # Use the Groq model specified in config.py [9].
        # Temperature is set to 0 to ensure consistent, deterministic classifications [10].
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model=config.GROQ_MODEL,
            temperature=0 
        )
        
        response_text = chat_completion.choices.message.content
        
        # Parsing logic: Extracts the tier from the "Tier: <tier>" format [4, 11].
        # It normalizes the string by stripping and lowercasing to avoid parsing errors [11, 12].
        tier = "unknown"
        for line in response_text.split('\n'):
            if line.strip().startswith("Tier:"):
                tier = line.replace("Tier:", "").strip().lower()
                break
        
        # Validation: Ensures the extracted tier is one of the allowed values [9, 12].
        if tier in config.VALID_TIERS:
            return tier
            
    except Exception:
        # If an error occurs or parsing fails, the system defaults to the safest fallback [4, 11, 13].
        pass

    return config.DEFAULT_FALLBACK_TIER
