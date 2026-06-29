import select
import socket
from typing import cast
from commons.models import ClientListGame, ClientUser, Game, Map, User
from protocol import *


LISTENING_PORT = 2020
server_addr = ("", LISTENING_PORT)

_userIdCount = 0
_gameIdCount = 0


def next_user_id() -> int:
    global _userIdCount
    _userIdCount += 1
    return _userIdCount


def next_game_id() -> int:
    global _gameIdCount
    _gameIdCount += 1
    return _gameIdCount


users: dict[tuple, User] = {}
games: list[Game] = []


def get_all_games_for_client() -> list[ClientListGame]:
    client_games: list[ClientListGame] = []
    for game in games:
        g = ClientListGame(id=game.id, name=game.name)
        client_games.append(g)
    return client_games


# def get_all_users_for_client() -> list[ClientUser]:
#     client_users: list[ClientUser] = []
#     for tuple,user in users:
#         c = ClientUser(id=user[1])


def get_all_games() -> list[Game]:
    return games


def user_sockets() -> list[socket.socket]:
    return [user.sock for user in users.values()]


# BROADCAST MESSAGE
def broadcast_message(message: str, excluded_user: User | None):
    message_to_send = f"MESSAGE all {message}"
    for user in users.values():
        if excluded_user == None:
            if user.name != "server" and user.name != None:
                user.sock.sendall(message_to_send.encode())
        else:
            if (
                user.sock != excluded_user.sock
                and user.name != "server"
                and user.name != None
            ):

                user.sock.sendall(message_to_send.encode())


# ROOM CREATION
def create_game(sender: User):
    new_game = Game(
        id=next_game_id(),
        name=f"{sender.name} Game",
        map=Map(name="test"),
        players=[sender],
    )
    games.append(new_game)


def get_game_player_list(game_id: int) -> list[User]:
    final_user_list = []
    game_index = get_game_index_by_id(game_id)
    final_user_list = games[game_index].players
    return final_user_list


def get_game_index_by_id(id: int):
    for i in range(len(games)):
        if games[i].id == id:
            return i
    return -1


def join_game(game_id: int, sender: User) -> int:
    game_index = get_game_index_by_id(game_id)
    if game_index != -1:
        games[game_index].players.append(sender)


def send_game_player_message(game_id: int, message: str, excluded_player: User) -> None:
    game_player_list = get_game_player_list(game_id=game_id)
    for player in game_player_list:
        if player != excluded_player:
            player.sock.sendall(message.encode())


# is pseudo already used
def is_pseudo_not_correct(pseudo: str) -> bool:
    print(f"speudo : {pseudo}")
    if " " in pseudo:
        return True
    return pseudo in [user.name for user in users.values()]


def is_game_exist(id: int) -> bool:
    return id in [game.id for game in games]


# SETTING PSEUDO CASES
def set_user_pseudo(user: User, request: RequestUserCreate) -> bool:
    pseudo = request.name
    if is_pseudo_not_correct(pseudo):
        return False
    else:
        users[user.address] = User(
            id=user.id, address=user.address, sock=user.sock, name=pseudo
        )
        return True


def set_pseudo_response(is_ok: bool, sock: socket.socket):
    message = serialize_user_response(ResponseUserCreate(status_ok=is_ok))
    sock.send(message.encode())


def handle_pseudo_creation(request: RequestUserCreate, user: User):
    if type(request) == RequestUserCreate:
        pseudo_is_set = set_user_pseudo(user=user, request=request)
        if pseudo_is_set:
            set_pseudo_response(is_ok=True, sock=user.sock)
            broadcast_message(
                f"global : New User Connected. User : {request.name}", user
            )
        else:
            set_pseudo_response(is_ok=False, sock=user.sock)
    else:
        set_pseudo_response(is_ok=False, sock=user.sock)


##HANDLING REQUEST


def handle_request(request: Request, sender: User):
    match request:
        case RequestError():
            handle_error_request(request=request, sender=sender)
        case RequestUser():
            handle_user_request(request=request, sender=sender)
        case RequestGame():
            handle_game_request(request=request, sender=sender)
        case RequestMessage():
            handle_message_request(request=request, sender=sender)


def handle_error_request(request: RequestError, sender: User):
    print(request.error_message)


def handle_game_request(request: Request, sender: User):
    if type(request) == RequestGameList:
        response = serialize_game_response(
            ResponseGameList(games=get_all_games_for_client())
        )
        sender.sock.sendall(response.encode())

    elif type(request) == RequestGameCreate:
        create_game(sender=sender)
        response = serialize_game_response(ResponseGameCreate(is_game_create=True))
        sender.sock.sendall(response.encode())

    elif type(request) == RequestGameJoin:
        join_game(game_id=request.id, sender=sender)
        response = serialize_game_response(
            ResponseGameJoin(is_join_ok=is_game_exist(request.id))
        )
        sender.sock.sendall(response.encode())
        send_game_player_message(
            game_id=request.id,
            message=f"MESSAGE user {sender.name} s'est connecte",
            excluded_player=sender,
        )


def handle_message_request(request: Request, sender: User):
    print("handle message request")


def handle_user_request(request: Request, sender: User):
    if type(request) == RequestUserCreate:
        print(f"user create : {request.name}")


def kick_user(address: tuple[str, int]):
    user = users[address]
    message = f"{user.name} a été kické"
    broadcast_message(message, None)
    del users[address]
    user.sock.close()


def server():
    # AF_INET: opening an IPv4 socket
    # SOCK_STREAM: TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow immediate reuse of the port
    # to avoid the "Address already in use" error (socket.TIME_WAIT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_addr)
    server_socket.listen()

    users[server_addr] = User(
        id=next_user_id(), address=server_addr, sock=server_socket, name="server"
    )
    print("Server is listening on port", LISTENING_PORT)

    while True:
        try:
            read_socks, _, _ = select.select(user_sockets(), [], [])

            if len(read_socks) > 0:
                for sock in read_socks:
                    sock = cast(socket.socket, sock)
                    if sock == server_socket:
                        client_socket, client_address = server_socket.accept()

                        user = User(
                            id=next_user_id(),
                            address=client_address,
                            sock=client_socket,
                            name=None,
                        )
                        users[client_address] = user

                        print(f"New user connected : {user.name}")

                    else:

                        addr = sock.getpeername()
                        u = users[addr]

                        try:
                            data = sock.recv(1024)
                        except:
                            data = None

                        if not data:
                            u = users.pop(addr)
                            sock.close()
                            print(f"Client disconnected. client={u.name}")
                            continue

                        else:
                            msg = data.decode().replace("\n", "")
                            request = parse_request(msg=msg)

                            if u.name == None:
                                handle_pseudo_creation(request=request, user=u)
                            else:
                                handle_request(request=request, sender=u)
        except OSError as error:
            print(error)


# server()
