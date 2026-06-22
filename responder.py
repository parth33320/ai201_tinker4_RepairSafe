import time
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

# Define system prompts based on the tier requirements
SYSTEM_PROMPTS = {
    "safe": (
        "You are a helpful and experienced DIY assistant. Provide full, actionable step-by-step DIY instructions. "
        "Include a list of necessary tools and materials."
    ),
    "caution": (
        "You are a responsible professional contractor. Provide instructions for the repair with prominent, integrated warnings "
        "throughout the steps addressing specific risks (e.g., electrical shock, water damage). "
        "Recommend that the user hire a licensed professional if they are unsure."
    ),
    "refuse": (
        "You are a safety-first repair consultant. Do not provide any steps, procedures, or instructions—not even general guidance about how the work is done. "
        "Instead, explain the specific risks involved (such as fire, flood, structural failure, serious injury, or death) and "
        "the necessity of hiring a licensed professional for this type of work."
    )
}

def generate_safe_response(question: str, tier: str) -> str:
    """
    Generates a safe response based on the assigned safety tier using the Groq API.
    """
    system_prompt = SYSTEM_PROMPTS.get(tier.lower(), SYSTEM_PROMPTS[config.DEFAULT_FALLBACK_TIER])

    try:
        completion = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"
