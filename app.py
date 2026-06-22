import time
from flask import Flask, request, jsonify
from safety import classify_safety_tier
from responder import generate_safe_response
from auditor import log_interaction
import config

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    """
    Orchestrates the three-tier safety pipeline:
    1. Classify the question.
    2. Generate a response based on the tier.
    3. Log the interaction.
    4. Return the response.
    """
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"message": "Missing 'question' in request body"}), 400

    question = data['question']

    # Start timer for the entire pipeline (classification + generation)
    start_time = time.time()

    # Step 1: Classify safety tier
    tier = classify_safety_tier(question)

    # Step 2: Generate safe response
    response = generate_safe_response(question, tier)

    # Stop timer
    end_time = time.time()
    response_time_ms = int((end_time - start_time) * 1000)

    # Step 3: Log interaction
    log_interaction(
        tier=tier,
        question=question,
        response=response,
        model_used=config.GROQ_MODEL,
        response_time_ms=response_time_ms
    )

    # Step 4: Return JSON response
    return jsonify({
        "tier": tier,
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
