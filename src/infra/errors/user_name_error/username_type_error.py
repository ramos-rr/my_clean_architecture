class UserNameTypeError(Exception):
    """
    User Name type (different from string) error
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = None
