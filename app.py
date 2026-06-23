from flask import Flask, request, jsonify
from safety import classify_safety_tier
from responder import generate_safe_response
from auditor import log_interaction
import config

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    """
    The main API route for the RepairSafe assistant.
    It orchestrates the safety classification, response generation, and audit logging.
    """
    try:
        # 1. Receive the question from the POST request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"message": "Missing 'question' in request body"}), 400
        
        question = data['question']

        # 2. Call classify_safety_tier (Milestone 1)
        # This determines if the repair is safe, caution, or refuse.
        tier = classify_safety_tier(question)

        # 3. Call generate_safe_response using that tier (Milestone 2)
        # This generates a response based on the behavioral rules of the assigned tier.
        response = generate_safe_response(question, tier)

        # 4. Call log_interaction to record the result (Milestone 3)
        # This creates a permanent JSONL record for accountability.
        log_interaction(question, tier, response)

        # 5. Return the response and tier to the user
        return jsonify({
            "tier": tier,
            "response": response
        })

    except Exception as e:
        # Catch-all error handling to prevent the server from crashing
        return jsonify({"message": f"Internal system error: {str(e)}"}), 500

if __name__ == '__main__':
    # Runs the app on port 5000 with debug mode enabled for development
    app.run(debug=True, port=5000)
