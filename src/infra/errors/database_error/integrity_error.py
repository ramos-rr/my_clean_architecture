class IntegrityError(Exception):
    def __init__(self, message: any, code: any) -> None:
        """
        Class to raise Integrity Error
        """
        super().__init__(message, code)
        self.message = message
        self.status_code = code
