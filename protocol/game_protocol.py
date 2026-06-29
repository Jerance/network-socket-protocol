from dataclasses import dataclass
from dataclasses_json import dataclass_json, config
from enum import Enum
from commons.models import ClientListGame, Game, game_to_json
from commons.utils import format_request_response
from commons.utils import game_protocol_utils
from commons.utils.game_protocol_utils import *
from protocol.error_protocol import RequestError
from protocol.protocol_commons import Request, Response


class GameEnumAttr(Enum):
    JOIN = "join"
    CREATE = "create"
    DELETE = "delete"
    LIST = "list"
    READY = "ready"
    STATE = "state"
    PLAY = "play"


class RequestGame(Request):
    pass


class ResponseGame(Response):
    pass


@dataclass(kw_only=True)
class RequestGameList(RequestGame):
    pass


@dataclass(kw_only=True)
class ResponseGameList(ResponseGame):
    games: list[ClientListGame]
    pass


@dataclass(kw_only=True)
class RequestGameCreate(RequestGame):
    pass


@dataclass(kw_only=True)
class ResponseGameCreate(ResponseGame):
    is_game_create: bool
    pass


@dataclass(kw_only=True)
class RequestGameJoin(RequestGame):
    id: int


@dataclass(kw_only=True)
class ResponseGameJoin(ResponseGame):
    is_join_ok: bool
    pass


# client prepare response to send to server
def serialize_game_request(request: RequestGame) -> str:
    match request:
        case RequestGameList():
            return f"GAME {GameEnumAttr.LIST.value}"
        case RequestGameCreate():
            return f"GAME {GameEnumAttr.CREATE.value}"
        case RequestGameJoin():
            return f"GAME {GameEnumAttr.JOIN.value} {request.id}"


# server transform request string from client into Request()
def parse_game_request(word_list: list[str]) -> Request:

    if len(word_list) < 2:
        return RequestError(
            error_message="Request Format Error: Missing Attribut. Status Code 1"
        )
    attr = word_list[1]
    match attr:
        case GameEnumAttr.LIST.value:
            return RequestGameList()
        case GameEnumAttr.CREATE.value:
            return RequestGameCreate()
        case GameEnumAttr.JOIN.value:
            if len(word_list) < 3:
                return RequestError(
                    error_message="Request Format Error: Missing content"
                )
            return RequestGameJoin(id=int(word_list[2]))

        case _:
            return RequestError(error_message="Request Format Error: Bad Attribut")


# client transform response string from server into Response()
def parse_game_response(word_list: list[str]) -> Response:

    if len(word_list) < 2:
        return RequestError(
            error_message="Response Format Error: Missing Attribut. Status Code 1"
        )
    attr = word_list[1]
    match attr:
        case GameEnumAttr.LIST.value:
            return ResponseGameList(
                games=transform_message_to_client_list_game(word_list[2])
            )
        case GameEnumAttr.CREATE.value:
            is_ok = True if word_list[2] == "True" else False
            return ResponseGameCreate(is_game_create=is_ok)
        case GameEnumAttr.JOIN.value:
            is_ok = True if word_list[2] == "True" else False
            return ResponseGameJoin(is_join_ok=is_ok)


# server prepare response to client
def serialize_game_response(response: Response) -> str:
    match response:
        case ResponseGameList():
            return f"GAME {GameEnumAttr.LIST.value} {transform_game_list_to_string(response.games)}"
        case ResponseGameCreate():
            return f"GAME {GameEnumAttr.CREATE.value} {response.is_game_create}"
        case ResponseGameJoin():
            return f"GAME {GameEnumAttr.JOIN.value} {response.is_join_ok}"
