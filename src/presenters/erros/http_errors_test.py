from .http_errors import HttpErrors


def test_http_error_422():
    error = HttpErrors.error_422('details for error 422')
    assert error["status_code"] == 422
    assert error["body"]['error']
    assert error["body"]['detail']


def test_http_error_400():
    error = HttpErrors.error_400('details for error 400')
    assert error["status_code"] == 400
    assert error["body"]['error']
    assert error["body"]['detail']
