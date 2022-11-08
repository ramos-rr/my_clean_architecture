class NoResultFoundError(Exception):
    def __init__(self, message: str = None, code: any = None) -> None:
        """
        Error to indicate that no result was found with the provided data
        """
        super().__init__(message)
        self.message = message
        self.status_code = code
