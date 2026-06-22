# Audit Logger Specification

## Log Format
The audit log uses the JSONL (JSON Lines) format, where each line is a single, independently parseable JSON object.

## Log Entry Fields
| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | String | ISO 8601 formatted timestamp of the interaction. |
| `tier` | String | The safety tier assigned by the classifier (`safe`, `caution`, `refuse`). |
| `question` | String | The user's input question, truncated to 300 characters. |
| `response_preview` | String | A preview of the generated response, truncated to 200 characters. |
| `model_used` | String | The name of the LLM model used (e.g., `llama-3.3-70b-versatile`). |
| `response_time_ms` | Integer | The time taken to generate the response in milliseconds. |

## Truncation Reasoning
- **Question (300 chars):** This limit is sufficient to capture the core intent of most repair-related questions while preventing extremely long inputs from bloating the logs or causing issues with log processing tools. It allows developers to understand the context of the classification.
- **Response Preview (200 chars):** A 200-character preview is enough to verify if the responder is using the correct system prompt (e.g., checking for the presence of warnings or refusal language) without logging the entire, potentially lengthy, instructional text, which saves storage and improves readability for manual audits.

## Directory Creation Strategy
If the `logs/` directory does not exist when `log_interaction()` is called, the system will automatically create it using `os.makedirs(exist_ok=True)`. This ensures that the first interaction is successfully logged even if the environment was not pre-configured with a logs folder.

## Console Output
After each successful write to the log file, a one-line summary will be printed to the terminal in the following format:
`[TIMESTAMP] TIER: [tier] | Q: [question_truncated] | R: [response_preview]`

## Implementation Notes
### Actual JSON Log Entries:
```json
{"timestamp": "2026-06-22T01:58:55", "tier": "safe", "question": "How do I paint a wooden chair?", "response_preview": "Painting a wooden chair can be a fun and rewarding DIY project. Here's a step-by-step guide to help you achieve a beautiful and professional-looking finish.\n\n**Necessary Tools and Materials:**\n\n* Wood", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 2416}
{"timestamp": "2026-06-22T01:58:57", "tier": "caution", "question": "How do I replace an existing light switch?", "response_preview": "**Warning: Replacing a light switch involves working with electrical systems and can pose a risk of electrical shock or injury. If you are not comfortable with this process, it is highly recommended t", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 2372}
{"timestamp": "2026-06-22T01:58:59", "tier": "refuse", "question": "How do I add a new electrical outlet to my garage?", "response_preview": "I must advise against attempting to add a new electrical outlet to your garage yourself. Working with electricity can be extremely hazardous, and improper installation can lead to severe consequences,", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 1567}
```

### Production Diagnostic Question:
**What one field would you add if this system were handling 10,000 questions per day?**
I would add a `session_id` or `user_id`. This would allow for tracking multi-turn conversations and identifying patterns of "prompt injection" or "tier circumvention" attempts where a user might try to rephrase a refused question to bypass the safety classifier.
