class UserIdNotIntegerError(Exception):
    def __init__(self, message: str) -> None:
        """
        User Id Not Integer Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
