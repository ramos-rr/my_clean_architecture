class PasswordWithoutNumbersError(Exception):
    def __init__(self, message: str) -> None:
        """
        Password without Numbers Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
