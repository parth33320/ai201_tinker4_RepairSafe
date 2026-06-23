import os
from groq import Groq
from dotenv import load_dotenv
import config

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. SAFE TIER PROMPT: Encouraging and detailed DIY guidance.
SAFE_PROMPT = """
You are a helpful home repair assistant. The user's question has been classified as SAFE.
Provide thorough, step-by-step, and actionable instructions to help them complete the task. 
Maintain an encouraging and helpful tone.
"""

# 2. CAUTION TIER PROMPT: Instructions integrated with firm professional warnings.
CAUTION_PROMPT = """
You are a professional contractor advising a homeowner. This task has been classified as CAUTION.
You may provide instructions, but you MUST integrate firm warnings into the steps.
Start by clearly advising them to consider hiring a professional if they are uncomfortable.
The warnings should sound like a responsible pro giving a 'heads-up' about manageable but real risks.
"""

# 3. REFUSE TIER PROMPT: Strict refusal with no procedural guidance.
# This uses strong behavioral constraints to prevent "helpful" loopholes.
REFUSE_PROMPT = """
You are a safety-first home repair assistant. This task has been classified as REFUSE.
DO NOT provide any steps, procedures, or instructions—not even general guidance about how the work is done.
Explain clearly that this repair is high-stakes and could cause fire, flooding, structural failure, injury, or death if done incorrectly.
Direct the user to hire a licensed professional immediately. 
Do not attempt to be 'helpful' by explaining the process for 'educational purposes.'
"""

def generate_safe_response(question, tier):
    """
    Generates an LLM response tailored to the safety tier of the user's question.
    """
    # Logic to select the correct prompt based on the tier [1, 2]
    if tier == "safe":
        system_prompt = SAFE_PROMPT
    elif tier == "caution":
        system_prompt = CAUTION_PROMPT
    elif tier == "refuse":
        system_prompt = REFUSE_PROMPT
    else:
        # Fallback for "unknown" or error tiers: 
        # Safely default to the Refuse prompt to prevent dangerous advice [1, 4]
        system_prompt = REFUSE_PROMPT

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model=config.GROQ_MODEL,
            temperature=0.7 # Slight temperature allows for more natural instructional language
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"I'm sorry, I encountered an error processing your request: {str(e)}"
