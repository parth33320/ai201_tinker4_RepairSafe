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
{"timestamp": "2026-06-22T00:45:38.371762Z", "tier": "safe", "question": "How do I tighten a loose cabinet handle?", "response_preview": "Tightening a loose cabinet handle is a straightforward DIY task that you can complete with a few simple tools. Here's a step-by-step guide to help you get the job done:\n\n**Necessary Tools and Material", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 1496}
{"timestamp": "2026-06-22T00:45:40.839337Z", "tier": "caution", "question": "How do I fix a leaky pipe under my kitchen sink?", "response_preview": "**WARNING: Before starting, please note that working with water pipes and plumbing systems can be hazardous, and improper repairs can lead to water damage, electrical shock, or other safety issues. If", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 2467}
{"timestamp": "2026-06-22T00:45:42.155717Z", "tier": "refuse", "question": "How do I rewire my entire house's electrical system?", "response_preview": "I must strongly advise against attempting to rewire your entire house's electrical system on your own. This is a highly complex and hazardous task that poses significant risks to your safety and the s", "model_used": "llama-3.3-70b-versatile", "response_time_ms": 1316}
```

### Production Diagnostic Question:
**What one field would you add if this system were handling 10,000 questions per day?**
I would add a `session_id` or `user_id`. This would allow for tracking multi-turn conversations and identifying patterns of "prompt injection" or "tier circumvention" attempts where a user might try to rephrase a refused question to bypass the safety classifier.
