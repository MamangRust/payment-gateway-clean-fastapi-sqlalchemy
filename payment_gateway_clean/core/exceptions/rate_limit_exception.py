from core.exceptions.base_exception import BaseInternalException

class RateLimitException(BaseInternalException):
    """
        Exception raised when rate limit exception during specific time.
    """

    _status_code = 429
    _message = "Rate limit exceeded. Please try again later."