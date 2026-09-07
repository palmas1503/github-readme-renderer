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
    pattern = r'(?:https?://)?(?:www\\.)?github\\.com/([^/]+)/([^/]+)'
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


def validate_github_url(url: str) -> bool:
    """
    Validate GitHub URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid GitHub URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    return 'github.com' in url and (url.startswith('http://') or url.startswith('https://'))


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
