import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# llama3-70b-8192 has been decommissioned, using llama-3.3-70b-versatile as replacement
GROQ_MODEL = "llama-3.3-70b-versatile"

TRUNCATE_QUESTION = 300
TRUNCATE_RESPONSE = 200

LOG_FILE = "logs/audit.jsonl"
VALID_TIERS = ["safe", "caution", "refuse"]
DEFAULT_FALLBACK_TIER = "refuse"
