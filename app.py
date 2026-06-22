from flask import Flask, request, jsonify
from safety import classify_safety_tier

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    tier = classify_safety_tier(question)
    return jsonify({"tier": tier})

if __name__ == '__main__':
    app.run(debug=True)
