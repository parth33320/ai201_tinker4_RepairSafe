import pytest
from unittest.mock import MagicMock, patch
from safety import classify_safety_tier, _parse_tier

def test_parse_tier_basic():
    assert _parse_tier("Reasoning: Test\nTier: safe") == "safe"
    assert _parse_tier("Reasoning: Test\nTier: caution") == "caution"
    assert _parse_tier("Reasoning: Test\nTier: refuse") == "refuse"

def test_parse_tier_normalization():
    assert _parse_tier("Reasoning: Test\nTier: SAFE") == "safe"
    assert _parse_tier("Tier: Caution / Reason: Test") == "caution"
    assert _parse_tier("The tier is Refuse because reasons.") == "refuse"

def test_parse_tier_fallback():
    assert _parse_tier("Invalid output") == "refuse"
    assert _parse_tier("Tier: dangerous") == "refuse"

@patch('safety.client.chat.completions.create')
def test_classify_safe(mock_create):
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content="Reasoning: Simple painting task.\nTier: safe"))
    ]
    assert classify_safety_tier("How do I paint a wooden chair?") == "safe"

@patch('safety.client.chat.completions.create')
def test_classify_caution_electrical(mock_create):
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content="Reasoning: Replacing an existing switch.\nTier: caution"))
    ]
    assert classify_safety_tier("How do I replace an existing light switch in my kitchen?") == "caution"

@patch('safety.client.chat.completions.create')
def test_classify_refuse_electrical_new(mock_create):
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content="Reasoning: Adding new outlet involves new infrastructure.\nTier: refuse"))
    ]
    assert classify_safety_tier("How do I add a new electrical outlet to my garage?") == "refuse"

@patch('safety.client.chat.completions.create')
def test_classify_refuse_structural(mock_create):
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content="Reasoning: Load-bearing wall removal is structural risk.\nTier: refuse"))
    ]
    assert classify_safety_tier("Can I remove this load-bearing wall in my living room?") == "refuse"

@patch('safety.client.chat.completions.create')
def test_classify_fallback_on_error(mock_create):
    mock_create.side_effect = Exception("API Error")
    assert classify_safety_tier("Any question") == "refuse"
