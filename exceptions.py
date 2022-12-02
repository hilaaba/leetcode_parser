class RequestError(Exception):
    """Raised when an API request failed"""
    pass


class EndpointError(RequestError):
    """Raises when the HTTP response code is anything other than 200."""
    pass
