class PasswordTypeError(Exception):
    def __init__(self, message: str) -> None:
        """
        Password Type error - Not string
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
