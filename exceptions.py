class EndpointError(Exception):
    """Возникает, когда код ответа HTTP отличный от 200."""

    pass


class RequestError(Exception):
    """Возникает, когда не удалось выполнить запрос к API."""

    pass
