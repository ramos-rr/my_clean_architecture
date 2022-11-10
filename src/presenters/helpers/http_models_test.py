from .http_models import HttpRequest, HttpResponse


def test_http_request():
    init = HttpRequest()
    assert 'header' in init.__dict__.keys()
    assert 'header' in init.__repr__()
    assert 'body' in init.__dict__.keys()
    assert 'body' in init.__repr__()
    assert 'query' in init.__dict__.keys()
    assert 'query' in init.__repr__()


def test_http_response():
    init = HttpResponse(0, 'a')
    assert 'status_code' in init.__dict__.keys()
    assert 'status_code' in init.__repr__()
    assert 'body' in init.__dict__.keys()
    assert 'body' in init.__repr__()
