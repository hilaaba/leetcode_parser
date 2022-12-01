class EndpointError(Exception):
    """Raises when the HTTP response code is anything other than 200."""
    pass


class RequestError(Exception):
    """Raised when an API request failed"""
    pass
