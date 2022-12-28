from typing import Type
from src.presenters.interface import RouteInterface as Route
from src.presenters.helpers import HttpRequest


def flask_adapter(request: any, api_route: Type[Route]) -> any:
    """
    Adapter patterns to flask
    :param request: Flask Request
    :param api_route: Composite route
    return: Any
    """

    headers = __get_headers(request=request)
    body = __get_body(request=request)
    query = __get_query(request=request)

    http_request = HttpRequest(header=headers, body=body, query=query)
    response = api_route.route(http_request=http_request)

    return response


def __get_headers(request) -> any:
    headers = None
    try:
        headers = request.headers
    except:
        pass
    return headers


def __get_body(request) -> any:
    body = None
    try:
        body = request.json
    except:
        try:
            body = request.body
        except:
            return body
        else:
            try:
                if "user_id" in body:
                    user_id = body.get("user_id")
                    if user_id:
                        try:
                            body["user_id"] = int(body["user_id"])
                        except:
                            pass
                if "age" in body:
                    age = body.get("age")
                    if age:
                        try:
                            body["age"] = int(body["age"])
                        except:
                            pass
            except:
                return body
            else:
                return body
    return body


def __get_query(request) -> any:
    try:
        query_string = request.args.to_dict()
    except:
        try:
            query_string = request.args
        except:
            try:
                query_string = request.query  # For requests coming from "/auth" route
            except:
                return dict()
            else:
                return query_string
        else:
            return query_string
    else:
        if len(query_string) == 0:
            return dict()
        else:
            query = dict()

            if "user_id" in query_string:
                try:
                    query["user_id"] = int(query_string.get("user_id"))
                except:
                    query["user_id"] = query_string.get("user_id")

            if "pet_id" in query_string:
                try:
                    query["pet_id"] = int(query_string.get("pet_id"))
                except:
                    query["pet_id"] = query_string.get("pet_id")

            if "username" in query_string:
                query["username"] = query_string.get("username")

            return query
