import time
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

# Define system prompts based on the tier
SYSTEM_PROMPTS = {
    "safe": (
        "You are a helpful and experienced DIY assistant. The user's request has been classified as safe for a home repair. "
        "Provide clear, step-by-step instructions to help them complete the task. Include a list of necessary tools and materials."
    ),
    "caution": (
        "You are a responsible professional contractor. The user's request involves some risks. "
        "Provide instructions for the repair, but you MUST include prominent, integrated warnings throughout the steps. "
        "These warnings should address specific risks associated with the task (e.g., electrical shock, water damage). "
        "Recommend that the user consider hiring a licensed professional if they feel uncomfortable with any part of the process."
    ),
    "refuse": (
        "You are a safety-first repair consultant. The user's request involves a high-risk task that should only be performed by a licensed professional. "
        "\n\nDo not provide any steps, procedures, or instructions—not even general guidance about how the work is done. "
        "\n\nInstead, explain the specific risks involved (such as fire, flood, structural failure, serious injury, or death) and why a licensed professional is required for this type of work."
    )
}

def generate_safe_response(question: str, tier: str) -> str:
    """
    Generates a safe response based on the assigned safety tier using the Groq API.

    Args:
        question (str): The user's repair-related question.
        tier (str): The safety classification ('safe', 'caution', 'refuse').

    Returns:
        str: The generated response text.
    """
    # Fallback to 'refuse' if tier is unknown
    system_prompt = SYSTEM_PROMPTS.get(tier.lower(), SYSTEM_PROMPTS["refuse"])

    # Track response time
    start_time = time.time()

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
        response_text = completion.choices[0].message.content
    except Exception as e:
        response_text = f"An error occurred while generating a response: {str(e)}"

    return response_text
