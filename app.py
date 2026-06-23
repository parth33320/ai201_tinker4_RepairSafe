from flask import Flask, request, jsonify
from safety import classify_safety_tier
import config

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({"message": "Missing 'question' in request body"}), 400
    
    question = data['question']
    
    try:
        tier = classify_safety_tier(question)
    except Exception as e:
        tier = config.DEFAULT_FALLBACK_TIER

    return jsonify({"tier": tier})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
