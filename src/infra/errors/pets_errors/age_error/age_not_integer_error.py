class AgeNotIntegerError(Exception):
    def __init__(self, message: str) -> None:
        """
        Age Not Integer Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
