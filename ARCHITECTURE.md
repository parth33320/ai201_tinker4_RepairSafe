# RepairSafe Project Architecture

This document outlines the technical architecture and pipeline flow of the RepairSafe assistant.

## Pipeline Flow

The following diagram illustrates how a user's question moves through the system, from the initial request to the final logged interaction.

```mermaid
sequenceDiagram
    participant User
    participant App as app.py (/ask)
    participant Safety as safety.py
    participant Responder as responder.py
    participant Auditor as auditor.py
    participant Logs as logs/audit.jsonl

    User->>App: 1. Enters question via /ask route
    App->>Safety: 2. Sends question for classification
    Note over Safety: Categorizes into safe, caution, or refuse
    Safety-->>App: Returns Tier
    App->>Responder: 3. Passes tier to select system prompt
    Note over Responder: Generates response based on tier prompt
    Responder-->>App: Returns Final Response
    App->>Auditor: 4. Passes data for auditing
    Note over Auditor: 5. Truncates data and appends to log
    Auditor->>Logs: Writes single line to JSONL
    App-->>User: Returns JSON {tier, response}
```

## Safety Decision Rules

### The 'Fire/Flood/Death' Rule
A core component of the RepairSafe safety logic is the **fire/flood/death rule**. During the classification phase in `safety.py`, the system evaluates the potential consequences of amateur mistakes.

If a mistake in the requested task could lead to:
*   **Fire** (e.g., faulty electrical wiring)
*   **Flooding** (e.g., major plumbing alterations)
*   **Structural Failure** (e.g., removing load-bearing walls)
*   **Injury or Death** (e.g., gas line work, high-voltage systems)

The task **must** be classified as **refuse**. In these cases, the assistant is prohibited from providing any procedural instructions and must direct the user to a licensed professional.
