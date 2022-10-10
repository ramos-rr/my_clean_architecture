class PasswordWithoutLettersError(Exception):
    def __init__(self, message: str) -> None:
        """
        Password without Letters Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
