class InsufficientDataError(Exception):
    def __init__(self, message: str) -> None:
        """
        Error to indicate Insufficient data to request DB valid information
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
