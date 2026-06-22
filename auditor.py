import json
import os
from datetime import datetime

LOG_FILE = "logs/audit.jsonl"

def log_interaction(tier: str, question: str, response: str):
    """
    Logs the interaction to an append-only JSONL file.
    Stub implementation.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tier": tier,
        "question": question[:300],
        "response_preview": response[:200]
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"Logged: {tier} - {question[:50]}...")
