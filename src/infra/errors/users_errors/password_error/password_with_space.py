class PasswordWithSpaceError(Exception):
    def __init__(self, message: str) -> None:
        """
        Password Type error - Spaces not allowed
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
