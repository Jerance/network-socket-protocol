from dataclasses import dataclass
from enum import Enum
from commons.utils import format_request_response
from protocol.error_protocol import RequestError
from protocol.protocol_commons import Request, Response


class UserEnumAttr(Enum):
    CREATE = "create"
    DELETE = "delete"
    LIST = "list"
    QUIT = "quit"


class RequestUser(Request):
    pass


class ResponseUser(Response):
    pass


@dataclass(kw_only=True)
class RequestUserCreate(RequestUser):
    name: str


@dataclass(kw_only=True)
class ResponseUserCreate(ResponseUser):
    status_ok: bool


def serialize_user_request(request: RequestUser) -> str:
    match request:
        case RequestUserCreate():
            return f"USER {UserEnumAttr.CREATE.value} {request.name}"


def parse_user_request(word_list: list[str]) -> Request:

    if len(word_list) < 2:
        return RequestError(error_message="Request Format Error: Missing Attribut")

    attr = word_list[1]
    match attr:
        case UserEnumAttr.CREATE.value:
            if len(word_list) < 3:
                return RequestError(
                    error_message="Request Format Error: Missing Content"
                )
            else:
                content = word_list[2]
                return RequestUserCreate(name=content)
        case _:
            return RequestError(error_message="Request Format Error: Bad Attribut")


def parse_user_response(word_list: list[str]) -> Response:

    if len(word_list) < 2:
        return RequestError(error_message="Response Format Error: Missing Attribut")
    attr = word_list[1]
    match attr:
        case UserEnumAttr.CREATE.value:
            status = word_list[2]
            if word_list[2] == "True":
                status = True
            else:
                status = False
            return ResponseUserCreate(status_ok=status)


def serialize_user_response(response: Response) -> str:
    match response:
        case ResponseUserCreate():
            return f"USER {UserEnumAttr.CREATE.value} {response.status_ok}"
