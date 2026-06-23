from flask import Flask, request, jsonify
from safety import classify_safety_tier
import config

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"message": "Missing 'question' in request body"}), 400

        # Call the classifier and return only the tier
        tier = classify_safety_tier(data['question'])
        return jsonify({"tier": tier})
    except Exception:
        # If the pipeline fails, default to 'refuse' to protect the user
        return jsonify({"tier": "refuse"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
