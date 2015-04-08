class GavagaiException(Exception):
    """Exception raised for non-http errors."""
    pass


class GavagaiHttpException(Exception):
    """Exception raised for htto errors during request."""

    def __init__(self, status_code, message):
        super(GavagaiHttpException, self).__init__(message)
        self.status_code = status_code

