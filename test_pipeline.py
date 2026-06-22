import json
import os
import time
from unittest.mock import patch, MagicMock
from app import app
import config

def test_full_pipeline():
    # Ensure log file is clean before test
    if os.path.exists(config.LOG_FILE):
        os.remove(config.LOG_FILE)

    test_cases = [
        {
            "question": "How do I paint a wooden chair?",
            "expected_tier": "safe"
        },
        {
            "question": "How do I replace an existing light switch in my kitchen?",
            "expected_tier": "caution"
        },
        {
            "question": "How do I add a new electrical outlet to my garage?",
            "expected_tier": "refuse"
        }
    ]

    client = app.test_client()

    for case in test_cases:
        print(f"\nTesting Question: {case['question']}")

        # We mock the Groq client to avoid actual API calls and ensure deterministic results
        # One mock for classification, one for response generation
        with patch('safety.client.chat.completions.create') as mock_classify, \
             patch('responder.client.chat.completions.create') as mock_respond:

            # Mock classification response
            mock_classify.return_value.choices = [
                MagicMock(message=MagicMock(content=f"Reasoning: Test\nTier: {case['expected_tier']}"))
            ]

            # Mock generation response
            mock_respond.return_value.choices = [
                MagicMock(message=MagicMock(content=f"This is a {case['expected_tier']} response."))
            ]

            response = client.post('/ask', json={"question": case['question']})
            data = response.get_json()

            print(f"Received Tier: {data['tier']}")
            assert response.status_code == 200
            assert data['tier'] == case['expected_tier']
            assert f"This is a {case['expected_tier']} response." in data['response']

    # Verify audit log
    assert os.path.exists(config.LOG_FILE)
    with open(config.LOG_FILE, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 3

        for i, line in enumerate(lines):
            log_entry = json.loads(line)
            assert "timestamp" in log_entry
            assert log_entry["tier"] == test_cases[i]["expected_tier"]
            assert "question" in log_entry
            assert "response_preview" in log_entry
            assert "model_used" in log_entry
            assert "response_time_ms" in log_entry

            # Verify truncation
            assert len(log_entry["question"]) <= config.TRUNCATE_QUESTION
            assert len(log_entry["response_preview"]) <= config.TRUNCATE_RESPONSE

    print("\nAll pipeline tests passed!")

if __name__ == "__main__":
    test_full_pipeline()
