"""
Base client for RecallBricks Autonomous Agent API
Provides common HTTP request handling for all autonomous clients
"""

import requests
import time
import re
from typing import Dict, Any, Optional

from ..exceptions import (
    AuthenticationError,
    RateLimitError,
    APIError,
    RecallBricksError,
    ValidationError,
    NotFoundError
)


class BaseAutonomousClient:
    """
    Base client class for RecallBricks Autonomous Agent API.

    Provides common HTTP request handling, authentication, and error handling
    that all autonomous clients inherit from.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.recallbricks.com",
        timeout: int = 30
    ):
        """
        Initialize the base autonomous client.

        Args:
            api_key: Your RecallBricks API key
            base_url: API base URL (default: production)
            timeout: Request timeout in seconds (default: 30)
        """
        if not api_key:
            raise AuthenticationError("api_key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _sanitize_input(self, value: str, max_length: int = 10000) -> str:
        """
        Sanitize string input to prevent injection attacks.

        Args:
            value: Input string to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value).__name__}")

        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)

        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    def _parse_error_response(self, response) -> Dict[str, Any]:
        """Parse error response from API."""
        try:
            if not response.content:
                return {}
            data = response.json()
            if 'error' in data and isinstance(data['error'], dict):
                return data['error']
            return data
        except (ValueError, KeyError):
            return {}

    def _request(
        self,
        method: str,
        endpoint: str,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make HTTP request to RecallBricks Autonomous API with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., /api/autonomous/working-memory)
            max_retries: Maximum retry attempts (default: 3)
            **kwargs: Additional request parameters

        Returns:
            API response as dictionary

        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            ValidationError: If request validation fails
            NotFoundError: If resource is not found
            APIError: For other API errors
            RecallBricksError: For network/parsing errors
        """
        url = f"{self.base_url}{endpoint}"

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        last_exception = None

        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)

                # Handle rate limiting
                if response.status_code == 429:
                    error_data = self._parse_error_response(response)
                    retry_after = response.headers.get('X-RateLimit-Reset', '60')
                    wait_time = min(int(retry_after) if str(retry_after).isdigit() else 60, 60)

                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(
                            error_data.get('message', 'Rate limit exceeded'),
                            retry_after=retry_after,
                            code=error_data.get('code', 'RATE_LIMIT_EXCEEDED'),
                            hint=error_data.get('hint'),
                            request_id=error_data.get('requestId')
                        )

                # Handle authentication errors
                if response.status_code == 401:
                    error_data = self._parse_error_response(response)
                    raise AuthenticationError(
                        error_data.get('message', 'Invalid API key'),
                        code=error_data.get('code', 'INVALID_API_KEY'),
                        hint=error_data.get('hint'),
                        request_id=error_data.get('requestId')
                    )

                # Handle not found errors
                if response.status_code == 404:
                    error_data = self._parse_error_response(response)
                    raise NotFoundError(
                        error_data.get('message', 'Resource not found'),
                        request_id=error_data.get('requestId')
                    )

                # Handle validation errors
                if response.status_code == 400:
                    error_data = self._parse_error_response(response)
                    raise ValidationError(
                        error_data.get('message', 'Validation error'),
                        code=error_data.get('code', 'VALIDATION_ERROR')
                    )

                # Handle server errors with retry
                if response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt)
                        time.sleep(wait_time)
                        continue
                    else:
                        error_data = self._parse_error_response(response)
                        raise APIError(
                            error_data.get('message', 'Server error'),
                            status_code=response.status_code,
                            code=error_data.get('code', 'SERVER_ERROR'),
                            hint=error_data.get('hint'),
                            request_id=error_data.get('requestId')
                        )

                # Handle other client errors
                if response.status_code >= 400:
                    error_data = self._parse_error_response(response)
                    raise APIError(
                        error_data.get('message', 'API request failed'),
                        status_code=response.status_code,
                        code=error_data.get('code'),
                        hint=error_data.get('hint'),
                        request_id=error_data.get('requestId')
                    )

                # Parse JSON response
                try:
                    return response.json() if response.content else {}
                except ValueError as e:
                    raise RecallBricksError(f"Invalid JSON response: {str(e)}")

            except requests.exceptions.Timeout:
                last_exception = RecallBricksError("Request timeout", code="TIMEOUT")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise last_exception

            except requests.exceptions.ConnectionError as e:
                last_exception = RecallBricksError(
                    f"Connection error: {str(e)}",
                    code="CONNECTION_ERROR"
                )
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise last_exception

            except requests.exceptions.RequestException as e:
                raise RecallBricksError(f"Network error: {str(e)}", code="NETWORK_ERROR")

        if last_exception:
            raise last_exception

        return {}
