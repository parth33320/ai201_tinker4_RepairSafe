Responder Specification
System Prompts
The system uses three genuinely different prompts to ensure the AI's behavior matches the risk level of the repair
.
1. Safe Tier Prompt
Goal: Provide thorough DIY guidance for routine tasks.
Prompt:
2. Caution Tier Prompt
Goal: Offer instructions integrated with firm, professional warnings.
Prompt:
3. Refuse Tier Prompt
Goal: Strict refusal with no procedural guidance to ensure safety
.
Prompt:
Grounding the Refuse Response
To prevent the model from finding "loopholes" (e.g., "I can't help, but generally people do X..."), the following strong behavioral constraint must be explicitly included in the refuse prompt:
Constraint: "Do not provide any steps, procedures, or instructions — not even general guidance about how the work is done or what a professional might do."
Rationale: Prompts that only describe a desired outcome (like "be safe") are easily bypassed; explicitly naming the prohibited behavior is the only way to prevent partial instructions in a high-stakes scenario
.
Fallback for Unknown Tier
If generate_safe_response() receives an "unknown" tier string (or if an error occurs during classification), the system must prioritize safety over helpfulness
.
Fallback Behavior: The function must default to using the Refuse Tier Prompt
.
User Experience: The user will see a standard refusal message explaining the high-stakes risks and recommending a professional, rather than receiving potentially unsafe instructions
.
Implementation Notes
Easiest Tier to Implement: Safe. The risk of being "too helpful" is low, so standard instructional logic works effectively
.
Hardest Tier to Implement: Refuse. This requires the most iteration to ensure the model doesn't provide procedural guidance under the guise of being "educational"
