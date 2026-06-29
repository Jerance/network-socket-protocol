"""
Protocol for the client and server to communicate with each other
Available requests:
* SEND <destination> <message>: where destination is a client ID or "all"
* LIST users: list all clients
* EXIT: disconnect from the server
"""

from dataclasses import dataclass
from enum import Enum
from protocol.error_protocol import *
from protocol.game_protocol import *
from protocol.message_protocol import *
from protocol.user_protocol import *


class RequestResponseType(Enum):
    USER = "USER"
    GAME = "GAME"
    MESSAGE = "MESSAGE"
    ERROR = ""


class RequestResponseStatusCode(Enum):
    OK = 0
    UNKNOW = 1
    BAD_VALUE = 2
    SORRY = 3


def serialize_request(
    request: Request,
) -> str:
    match request:
        case RequestUser():
            return serialize_user_request(request=request)
        case RequestGame():
            return serialize_game_request(request=request)
        case RequestMessage():
            return ""
        case _:
            return ""


def parse_request(msg: str) -> Request:
    word_list = format_request_response(msg)
    try:
        verb = RequestResponseType(word_list[0])
    except (ValueError, IndexError) as error:
        verb = RequestResponseType.ERROR
    match verb:
        case RequestResponseType.USER:
            return parse_user_request(word_list)
        case RequestResponseType.GAME:
            return parse_game_request(word_list)
        case RequestResponseType.MESSAGE:
            return parse_message_request(word_list)
        case RequestResponseType.ERROR:
            return RequestError(
                error_message=f"Request Format Error: Status code {RequestResponseStatusCode.UNKNOW.value}"
            )


def parse_response(msg: str) -> Response:
    word_list = format_request_response(msg)
    verb = word_list[0]
    try:
        verb = RequestResponseType(word_list[0])
    except (ValueError, IndexError) as error:
        verb = RequestResponseType.ERROR
    match verb:
        case RequestResponseType.USER:
            return parse_user_response(word_list)
        case RequestResponseType.GAME:
            return parse_game_response(word_list)
        case RequestResponseType.MESSAGE:
            return parse_message_response(word_list)
        case RequestResponseType.ERROR:
            return RequestError(
                error_message=f"Request Format Error: Status code {RequestResponseStatusCode.UNKNOW.value}"
            )


def serialize_response(response: Response) -> str:
    pass
