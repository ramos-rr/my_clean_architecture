class HttpErrors:
    """ Class to define which HTTP ERROR has occured """

    @staticmethod
    def error_400(detail: any = None):
        """
        Error HTTP 400
        :return: Error status code and body
        """

        return {"status_code": 400,
                "body":
                    {"error": "Bad request. The server can not process the request because it is not well formulated",
                     "detail": detail}
                }

    @staticmethod
    def error_422(detail: any = None):
        """
        Error HTTP 422
        :return: Error status code and body
        """

        return {"status_code": 422,
                "body":
                    {"error": "Unprocessable Entity. The server understands the request, the syntax is correct,"
                              " but it was unable to get a response. See the details next",
                     "detail": detail}
                }
