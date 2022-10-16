class PetIdNotIntegerError(Exception):
    def __init__(self, message: str) -> None:
        """
        Pet Id Not Integer Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
