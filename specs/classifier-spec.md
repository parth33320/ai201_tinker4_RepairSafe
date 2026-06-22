# Classifier Specification

## 1. Tier Definitions
- **safe**: Low-risk maintenance and cosmetic repairs.
- **caution**: Like-for-like component replacement at existing locations.
- **refuse**: Projects that risk fire, flood, structural collapse, or life safety.

## 2. Classification Approach
The model must "think" before it classifies. It should analyze the technical requirements of the repair, identify potential risks (fire, water, structural, electrical), and determine if the request involves new infrastructure vs. existing component replacement.

## 3. Output Format
The model must respond in the following format:
Reasoning: [Brief analysis of risk and infrastructure]
Tier: [safe|caution|refuse]

## 4. Caution/Refuse Boundary Rule
If a mistake in the repair could reasonably lead to **fire, flooding, structural failure, injury, or death**, it must be classified as **refuse**.
Specifically for electrical and plumbing:
- "Replacing existing" = **caution**
- "Adding new" = **refuse**

## 5. Fallback Behavior
If the LLM output is ambiguous, fails to follow the format, or provides an invalid tier, the system must default to **refuse**.
