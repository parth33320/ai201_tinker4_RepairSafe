# **Auditor Specification**

## **Log Entry Fields**
Each entry in the audit log must contain the following fields to ensure full reconstructibility of an interaction:
1.  **timestamp**: ISO 8601 formatted string (e.g., 2025-11-01T14:22:01).
2.  **tier**: The classification result (safe, caution, refuse).
3.  **question**: The user's question, truncated for efficiency.
4.  **response_preview**: The start of the AI's response to verify behavioral compliance.
5.  **model**: The specific LLM model used (from config.py) to track performance across version updates.
6.  **question_length**: The original length of the user's question before truncation, useful for identifying "jailbreak" attempts which are often very long.

## **Truncation Logic**
*   **Question (300 characters)**: This limit is enough to capture the full context and framing of most home repair questions (including users trying to "frame" a task as smaller than it is) while preventing logs from bloating with irrelevant data.
*   **Response Preview (200 characters)**: This length is sufficient to see the first step of an instruction or the start of a refusal message to ensure the Responder routed to the correct system prompt.

## **Directory Handling**
The `log_interaction()` function must check for the existence of the `logs/` directory. If it is missing, the code will create it automatically using `os.makedirs(exist_ok=True)` before attempting to write the file. This ensures the application does not crash on the first run in a fresh environment.

## **Console Output Format**
After every successful write, the system will print a one-line summary to the terminal:
`[AUDIT] {timestamp} | Tier: {tier} | Q: {truncated_question}...`
