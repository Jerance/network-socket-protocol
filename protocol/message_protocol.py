from dataclasses import dataclass
from enum import Enum
from protocol.error_protocol import RequestError

from protocol.protocol_commons import Request, Response


class MessageEnumAttr(Enum):
    USER = "user"
    ROOM = "room"
    ALL = "all"


class RequestMessage(Request):
    pass


class ResponseMessage(Response):
    pass


@dataclass(kw_only=True)
class RequestMessageAll(RequestMessage):
    message: str


@dataclass(kw_only=True)
class ResponseMessageAll(ResponseMessage):
    message: str


@dataclass(kw_only=True)
class RequestMessageUser(RequestMessage):
    pass


@dataclass(kw_only=True)
class ResponseMessageUser(ResponseMessage):
    message: str


def serialize_message_request(request: RequestMessage) -> str:
    pass


def parse_message_request(word_list: list[str]) -> Request:
    if len(word_list) < 2:
        return RequestError(
            error_message="Request Format Error: Missing Attribut. Status Code 1"
        )
    attr = word_list[1]
    match attr:
        case MessageEnumAttr.ALL.value:
            return RequestMessageAll(word_list[2])
        case _:
            return RequestError(error_message="Request Format Error: Bad Attribut")


def parse_message_response(word_list: list[str]) -> Response:
    if len(word_list) < 2:
        return RequestError(
            error_message="Request Format Error: Missing Attribut. Status Code 1"
        )
    attr = word_list[1]
    match attr:
        case MessageEnumAttr.ALL.value:
            if len(word_list) < 2:
                return RequestError(
                    error_message="Request Format Error: Missing Content"
                )
            return ResponseMessageAll(message=word_list[2])
        case MessageEnumAttr.USER.value:
            if len(word_list) < 2:
                return RequestError(
                    error_message="Request Format Error: Missing Content"
                )
            return ResponseMessageUser(message=word_list[2])
        case _:
            return RequestError(error_message="Request Format Error: Bad Attribut")


def serialize_message_response(response: Response) -> str:
    match response:
        case ResponseMessageAll():
            return f"MESSAGE {MessageEnumAttr.ALL.value} {response.message}"
