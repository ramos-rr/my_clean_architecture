from typing import Dict


class HttpRequest:
    """ Class to http_request representation """

    def __init__(self, header: Dict = None, body: Dict = None, query: Dict = None):
        self.header = header
        self.body = body
        self.query = query

    def __repr__(self):
        return f"HttpRequest (header={self.header}, body={self.body}, query={self.query})"


class HttpResponse:
    """ Class to http_response representation """

    def __init__(self, header: Dict = None, body: Dict = None, query: Dict = None):
        self.header = header
        self.body = body
        self.query = query

    def __repr__(self):
        return f"HttpResponse (header={self.header}, body={self.body}, query={self.query})"
