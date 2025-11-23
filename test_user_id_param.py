"""
Test user_id parameter in save() method
"""
from recallbricks import RecallBricks
from recallbricks.exceptions import RecallBricksError

def test_service_token_requires_user_id():
    """Test that service token auth requires user_id"""
    rb = RecallBricks(service_token="rbk_service_test123")

    # Should raise ValueError when user_id is not provided
    try:
        rb.save("Test memory without user_id")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "user_id is required when using service token" in str(e)
        print("[PASS] Service token requires user_id validation works")

def test_api_key_optional_user_id():
    """Test that API key auth allows optional user_id"""
    rb = RecallBricks(api_key="rb_dev_test123")

    # This should not raise an error (will fail at API level with invalid key, but validation passes)
    try:
        rb.save("Test memory without user_id")
    except RecallBricksError as e:
        # Expected to fail at API level due to invalid key
        # But should NOT fail validation for missing user_id
        if "user_id is required" in str(e):
            raise AssertionError("API key should not require user_id")
        print("[PASS] API key allows optional user_id")

def test_user_id_validation():
    """Test user_id validation"""
    rb = RecallBricks(service_token="rbk_service_test123")

    # Empty string should raise ValueError
    try:
        rb.save("Test memory", user_id="   ")
        assert False, "Should have raised ValueError for empty user_id"
    except ValueError as e:
        assert "user_id cannot be empty" in str(e)
        print("[PASS] Empty user_id validation works")

    # Non-string user_id should raise TypeError
    try:
        rb.save("Test memory", user_id=12345)
        assert False, "Should have raised TypeError for non-string user_id"
    except TypeError as e:
        assert "user_id must be a string" in str(e)
        print("[PASS] Non-string user_id validation works")

def test_user_id_included_in_payload():
    """Test that user_id is included in payload when provided"""
    import json
    from unittest.mock import Mock, patch

    rb = RecallBricks(service_token="rbk_service_test123")

    # Mock the session.request to capture the payload
    captured_payload = {}

    def mock_request(method, url, **kwargs):
        captured_payload.update(kwargs.get('json', {}))
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = True
        mock_response.json.return_value = {"id": "test123", "text": "Test"}
        return mock_response

    with patch.object(rb.session, 'request', side_effect=mock_request):
        rb.save("Test memory", user_id="user_456")

    assert captured_payload.get('user_id') == "user_456"
    print("[PASS] user_id is included in request payload")

if __name__ == "__main__":
    print("\nTesting user_id parameter implementation...\n")

    test_service_token_requires_user_id()
    test_api_key_optional_user_id()
    test_user_id_validation()
    test_user_id_included_in_payload()

    print("\n[SUCCESS] All user_id parameter tests passed!")
