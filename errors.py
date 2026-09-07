"""
Custom exception classes for the application
"""


class AppError(Exception):
    """Base application error"""
    
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "APP_ERROR"
        super().__init__(self.message)


class APIKeyError(AppError):
    """Raised when API key is missing or invalid"""
    
    def __init__(self, provider: str):
        message = f"{provider} API key not configured"
        super().__init__(message, status_code=401, error_code="API_KEY_ERROR")


class ValidationError(AppError):
    """Raised when input validation fails"""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR")


class ProviderError(AppError):
    """Raised when AI provider API fails"""
    
    def __init__(self, provider: str, status_code: int, message: str = None):
        msg = message or f"{provider} API returned status {status_code}"
        super().__init__(msg, status_code=502, error_code="PROVIDER_ERROR")


class TimeoutError(AppError):
    """Raised when API request times out"""
    
    def __init__(self, provider: str):
        message = f"{provider} API request timed out"
        super().__init__(message, status_code=504, error_code="TIMEOUT_ERROR")


class RateLimitError(AppError):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, provider: str, retry_after: int = None):
        message = f"{provider} API rate limit exceeded"
        super().__init__(message, status_code=429, error_code="RATE_LIMIT_ERROR")
        self.retry_after = retry_after


class NotFoundError(AppError):
    """Raised when resource is not found"""
    
    def __init__(self, resource: str):
        message = f"{resource} not found"
        super().__init__(message, status_code=404, error_code="NOT_FOUND_ERROR")
