import flet as ft
import socket

from client import connect_to_server, send_request
from commons.models import ClientListGame, Game
from protocol.error_protocol import ResponseError
from protocol.game_protocol import (
    RequestGameCreate,
    RequestGameJoin,
    RequestGameList,
    ResponseGame,
    ResponseGameCreate,
    ResponseGameJoin,
    ResponseGameList,
)
from protocol.message_protocol import (
    ResponseMessage,
    ResponseMessageAll,
    ResponseMessageUser,
)
from protocol.protocol_commons import Response
from protocol.user_protocol import RequestUserCreate, ResponseUser, ResponseUserCreate

SERVER_HOST = "localhost"

SERVER_PORT = 2020
client_socket: socket.socket | None = None

pseudo_ref = ft.Ref[ft.TextField]()
broadcast_area_ref = ft.Ref[ft.Text]()
container_ref = ft.Ref[ft.Container]()
screen2_ref = ft.Ref[(ft.Column)]()
rooms_ref = ft.Ref[ft.ListView]()

main_page: ft.Page | None = None
is_input_show = True

main_page = None


def on_click_pseudo_input(e):
    global is_input_show
    pseudo = pseudo_ref.current.value
    request = RequestUserCreate(name=pseudo)
    send_request(client_socket, request)
    pseudo_ref.current.value = ""
    pseudo_ref.current.update()


def on_click_get_rooms(e):
    request = RequestGameList()
    send_request(client_socket, request)


def on_create_room_click(e):
    request = RequestGameCreate()
    send_request(client_socket, request)


def on_join_room_click(id: int):
    request = RequestGameJoin(id=id)
    send_request(client_socket, request)


def on_message_response_received(response: ResponseMessage):
    match response:
        case ResponseMessageAll():
            broadcast_area_ref.current.value = response.message
            broadcast_area_ref.current.update()
        case ResponseMessageUser():
            broadcast_area_ref.current.value = response.message
            broadcast_area_ref.current.update()


def on_game_response_received(response: ResponseGame):
    match response:
        case ResponseGameList():
            for game in response.games:
                rooms_ref.current.controls.append(build_list_room_tile(game))
                rooms_ref.current.update()
        case ResponseGameCreate():
            if response.is_game_create:
                screen2_ref.current.controls = []
                screen2_ref.current.controls.append(build_room_container())
                screen2_ref.current.update()
        case ResponseGameJoin():
            if response.is_join_ok:
                screen2_ref.current.controls = []
                screen2_ref.current.controls.append(build_room_container())
                screen2_ref.current.update()


def on_user_response_received(response: ResponseUser):
    match response:
        case ResponseUserCreate():
            global is_input_show
            is_input_show = not response.status_ok
            if is_input_show != True:
                container_ref.current.content = build_main_screen()
                container_ref.current.update()
        case _:
            pass


def build_list_room_tile(game: ClientListGame):
    return ft.Row(
        expand=True,
        controls=[
            ft.ListTile(expand=True, title=ft.Text(game.name)),
            ft.ElevatedButton(
                text="Join", on_click=lambda event, g=game: on_join_room_click(g.id)
            ),
        ],
    )


def on_response_received(response: Response):
    match response:
        case ResponseUser():
            on_user_response_received(response)
        case ResponseGame():
            on_game_response_received(response)
        case ResponseMessage():
            on_message_response_received(response)
        case _:
            ResponseError(error_message="Unknown response type")


def build_room_container():
    return ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text("coucou")]),
            ft.Container(width=50, height=50, bgcolor="red"),
            ft.Row(controls=[ft.Text("coucou")]),
        ],
    )


def build_pseudo_row():
    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    ft.TextField(
                        expand=True,
                        ref=pseudo_ref,
                        hint_text="Pseudo",
                        autofocus=True,
                        on_submit=on_click_pseudo_input,
                    ),
                    ft.ElevatedButton("Create", on_click=on_click_pseudo_input),
                ],
            ),
        ],
    )


def build_main_screen():
    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                content=ft.Column(
                    ref=screen2_ref,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Create room", on_click=on_create_room_click
                                ),
                                ft.ElevatedButton(
                                    "get rooms", on_click=on_click_get_rooms
                                ),
                            ]
                        ),
                        ft.ListView(
                            ref=rooms_ref,
                            expand=True,
                            spacing=10,
                            auto_scroll=True,
                        ),
                    ],
                ),
            ),
            ft.Column(
                height=150,
                controls=[
                    ft.Text(expand=True, value="Serveur Messages : "),
                    ft.Text(expand=True, ref=broadcast_area_ref, value=""),
                ],
            ),
        ],
    )


def build_game_list(games: list[Game]):
    for game in games:
        return ft.Card(content=ft.Text(game.name))


def main(page):
    global client_socket
    global main_page
    main_page = page

    page.title = "Nouveau_Dossier.io"

    page_container = ft.Container(
        expand=True,
        ref=container_ref,
        # content=build_room_container(),
        content=build_pseudo_row(),
    )

    page.add(page_container)

    client_socket = connect_to_server(
        SERVER_HOST,
        SERVER_PORT,
        on_message=on_response_received,
    )


ft.app(target=main)
