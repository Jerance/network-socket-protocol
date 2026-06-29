import socket
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(kw_only=True)
class User:
    id: int
    address: tuple[str, int]
    # J'ai renommé le champ pour éviter la confusion avec le module socket
    # Il y a la conf spéciale à faire pour ignorer socket du JSON (lecture / écriture)
    sock: socket.socket
    name: str | None


@dataclass(kw_only=True)
class ClientUser:
    id: int
    name: str


@dataclass_json
@dataclass(kw_only=True)
class Tile:
    position: tuple[int, int]
    owner: User | None
    trailed_by: User | None
    occupied: bool


@dataclass_json
@dataclass(kw_only=True)
class Map:
    name: str
    # tiles: list[list[Tile]]


@dataclass_json
@dataclass(kw_only=True)
class Game:
    id: int
    name: str
    map: Map
    players: list[User]


@dataclass(kw_only=True)
class ClientListGame:
    id: int
    name: str


@dataclass_json
@dataclass(kw_only=True)
class Message:
    author: str
    content: str


def game_to_json(game: Game) -> str:
    json_data = game.to_json()
    return json_data
