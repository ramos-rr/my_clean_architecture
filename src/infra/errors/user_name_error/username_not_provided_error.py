class UserNameNotProvidedError(Exception):
    def __init__(self, message: str) -> None:
        """
        User Name Not Provided Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
