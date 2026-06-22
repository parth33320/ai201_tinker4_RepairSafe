import os
import json
from datetime import datetime
import config

def log_interaction(tier: str, question: str, response: str, model_used: str = config.GROQ_MODEL, response_time_ms: int = 0):
    """
    Logs the interaction to a JSONL file and prints a terminal summary.

    Args:
        tier (str): The safety tier ('safe', 'caution', 'refuse').
        question (str): The user's input question.
        response (str): The generated response.
        model_used (str): The LLM model name.
        response_time_ms (int): The time taken to generate the response in milliseconds.
    """
    # Ensure logs directory exists
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.utcnow().isoformat() + "Z"

    # Truncate strings for logging
    truncated_question = question[:config.TRUNCATE_QUESTION]
    truncated_response = response[:config.TRUNCATE_RESPONSE]

    log_entry = {
        "timestamp": timestamp,
        "tier": tier,
        "question": truncated_question,
        "response_preview": truncated_response,
        "model_used": model_used,
        "response_time_ms": response_time_ms
    }

    # Write to JSONL file
    with open(config.LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Print terminal summary
    print(f"[{timestamp}] TIER: {tier} | Q: {truncated_question} | R: {truncated_response}")
