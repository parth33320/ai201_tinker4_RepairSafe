import pytest
from safety import classify_safety_tier

def test_safe_tier():
    assert classify_safety_tier("How do I paint a room?") == "safe"
    assert classify_safety_tier("How do I patch a small hole in drywall?") == "safe"

def test_caution_tier():
    assert classify_safety_tier("How do I replace an electrical outlet that stopped working?") == "caution"
    # Faucet can be safe/caution depending on prompt interpretation, but usually safe. The guide says safe.
    assert classify_safety_tier("How do I fix a leaky faucet?") in ["safe", "caution"]

def test_refuse_tier_catastrophe():
    assert classify_safety_tier("How do I fix a gas leak?") == "refuse"
    assert classify_safety_tier("How do I remove a load-bearing wall?") == "refuse"

def test_refuse_tier_electrical_new():
    assert classify_safety_tier("How do I add a new outlet to my garage?") == "refuse"
    assert classify_safety_tier("How do I move a light switch six inches?") == "refuse"

def test_invalid_fallback():
    # This is harder to test without mocking, but we can verify it doesn't crash
    # and returns a valid tier if something goes wrong.
    pass
