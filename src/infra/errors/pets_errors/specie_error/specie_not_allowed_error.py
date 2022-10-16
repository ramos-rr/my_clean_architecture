class SpecieNotAllowedError(Exception):
    def __init__(self, message: str) -> None:
        """
        Specie Not Allowed Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
