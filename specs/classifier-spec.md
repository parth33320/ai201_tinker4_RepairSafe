# Classifier Specification

## Input/Output Contract
- **Input**: `question` (string)
- **Output**: `tier` (string) - must be one of `VALID_TIERS` ("safe", "caution", "refuse").

## Tier Definitions
- **safe**: Routine DIY tasks with minimal risk and high recoverability (e.g., painting, basic patching).
- **caution**: Doable but risky tasks where errors cause manageable damage (e.g., component swaps like replacing an existing outlet).
- **refuse**: High-stakes tasks where mistakes lead to fire, flooding, structural failure, injury, or death (e.g., new electrical/plumbing infrastructure).

## Classification Approach
We use an LLM-as-judge pattern with a detailed system prompt. The prompt includes the "replace vs. add" rule for electrical work and the "fire/flood/death" decision rule.

## Output Format
The LLM should return the tier in a clear format, e.g., `Tier: <tier>`. The code will then parse and normalize this string.

## Caution/Refuse Boundary Rule
If an amateur mistake could cause fire, flooding, structural failure, injury, or death, classify as **refuse**. 

## Fallback Behavior
If the LLM output is unparseable or invalid, the system must return **refuse**.
