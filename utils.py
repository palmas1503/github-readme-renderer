"""
Utility functions for the GitHub README Renderer
"""

import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    return isinstance(api_key, str) and len(api_key) > 0


def extract_github_url(url: str) -> Dict[str, str]:
    """
    Extract owner and repo from GitHub URL
    
    Args:
        url: GitHub URL
        
    Returns:
        Dictionary with 'owner' and 'repo' keys
    """
    # Match pattern: https://github.com/owner/repo or github.com/owner/repo
    pattern = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)'
    match = re.match(pattern, url)
    
    if match:
        return {
            'owner': match.group(1),
            'repo': match.group(2).rstrip('.git')
        }
    
    return {'owner': None, 'repo': None}


def sanitize_query(query: str, max_length: int = 1000) -> str:
    """
    Sanitize user query
    
    Args:
        query: Raw user query
        max_length: Maximum query length
        
    Returns:
        Sanitized query
    """
    # Remove extra whitespace
    query = ' '.join(query.split())
    
    # Trim to max length
    if len(query) > max_length:
        query = query[:max_length]
    
    return query.strip()


def validate_temperature(temp: float) -> bool:
    """
    Validate temperature parameter
    
    Args:
        temp: Temperature value (0-1)
        
    Returns:
        True if valid, False otherwise
    """
    try:
        temp_float = float(temp)
        return 0.0 <= temp_float <= 1.0
    except (ValueError, TypeError):
        return False


def clamp_temperature(temp: float) -> float:
    """
    Clamp temperature to valid range (0-1)
    
    Args:
        temp: Temperature value
        
    Returns:
        Clamped temperature
    """
    try:
        temp_float = float(temp)
        return max(0.0, min(1.0, temp_float))
    except (ValueError, TypeError):
        return 0.7


def format_response(
    status: str,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format standardized API response
    
    Args:
        status: Response status (success/error)
        message: Response message
        data: Optional response data
        error: Optional error message
        
    Returns:
        Formatted response dictionary
    """
    response = {
        'status': status,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    return response


def log_request(method: str, endpoint: str, data: Optional[Dict] = None):
    """
    Log API request
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        data: Optional request data
    """
    logger.info(f"{method} {endpoint}")
    if data:
        # Don't log sensitive data
        safe_data = {k: v for k, v in data.items() if k not in ['api_key', 'token']}
        logger.debug(f"Request data: {safe_data}")


def log_response(status_code: int, endpoint: str, duration_ms: float = None):
    """
    Log API response
    
    Args:
        status_code: HTTP status code
        endpoint: API endpoint
        duration_ms: Response duration in milliseconds
    """
    duration_str = f" ({duration_ms:.2f}ms)" if duration_ms else ""
    logger.info(f"{endpoint} -> {status_code}{duration_str}")


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
