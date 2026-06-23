import json
import os
from datetime import datetime
import config

# Define the log file location
LOG_FILE = "logs/audit.jsonl"

def log_interaction(question, tier, response):
    """
    Logs a single interaction to an append-only JSONL file.
    Each record is a single-line JSON object.
    """
    # 1. Directory Handling: Ensure the logs directory exists [2, 8]
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # 2. Field Truncation [7, 8]
    # Questions truncated to 300, responses to 200
    truncated_q = (question[:300] + '..') if len(question) > 300 else question
    truncated_res = (response[:200] + '..') if len(response) > 200 else response
    
    # 3. Create the log record
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "tier": tier,
        "question": truncated_q,
        "response_preview": truncated_res,
        "model": config.GROQ_MODEL,
        "original_q_len": len(question)
    }

    # 4. JSONL Writing [5, 8, 9]
    # Use json.dumps() to ensure a single line and append \n
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # 5. Console Output Summary [2, 8]
    print(f"[AUDIT] {timestamp} | Tier: {tier.upper()} | Q: {truncated_q[:50]}...")

if __name__ == "__main__":
    # Quick test of the logging logic
    log_interaction("How do I paint a wall?", "safe", "First, you should clean the surface...")
