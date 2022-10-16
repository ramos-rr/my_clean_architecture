class SpecieNotProvidedError(Exception):
    def __init__(self, message: str) -> None:
        """
        Specie Not Provided Error
        """
        super().__init__(message)
        self.message = message
        self.status_code = None
