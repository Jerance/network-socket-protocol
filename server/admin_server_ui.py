import flet as ft
import socket
from client.client import connect_to_server, send_request

from protocol.error_protocol import ResponseError
from protocol.message_protocol import (
    ResponseMessage,
    ResponseMessageAll,
)
from protocol.protocol_commons import Response
import server

SERVER_HOST = "localhost"

SERVER_PORT = 2020
client_socket: socket.socket | None = None


messages_ref = ft.Ref[ft.ListView]()
input_ref = ft.Ref[ft.TextField]()
users_ref = ft.Ref[ft.ListView]()
rooms_ref = ft.Ref[ft.ListView]()

users = server.users
rooms_game = server.games


def on_game_response_received(response: ResponseMessage):
    match response:
        case ResponseMessageAll():
            pass


def refresh_all_users_game_rooms(e):
    users_ref.current.controls = []
    for user in users.values():
        if user.name != "server":
            users_ref.current.controls.append(
                ft.Row(
                    expand=True,
                    controls=[
                        ft.ListTile(
                            expand=True,
                            title=ft.Text(
                                f"id: {user.id} name: {user.name} / address: {user.address}"
                            ),
                            leading=ft.Icon("person"),
                        ),
                        ft.ElevatedButton(
                            "Kick",
                            on_click=lambda event, u=user: server.kick_user(u.address),
                        ),
                    ],
                ),
            )
            users_ref.current.update()

    rooms_ref.current.controls = []
    for room in rooms_game:
        rooms_ref.current.controls.append(
            ft.Row(
                expand=True,
                controls=[
                    ft.ListTile(
                        expand=True,
                        title=ft.Text(f"{room.name}"),
                    ),
                ],
            ),
        )
        rooms_ref.current.update()


def on_response_received(response: Response):
    print(f"on_response_received. message={response}")
    match response:
        case ResponseMessageAll():
            on_game_response_received(response)
        case _:
            ResponseError(error_message="Unknown response type")


def on_send_clicked(e):
    message = input_ref.current.value

    on_response_received(f"Me: {message}")
    input_ref.current.value = ""
    input_ref.current.update()
    input_ref.current.focus()

    server.broadcast_message(message=message, excluded_user=None)


def build_chat_column():
    return ft.Column(
        expand=True,
        width=600,
        controls=[
            ft.ListView(
                ref=messages_ref,
                expand=True,
                spacing=10,
                auto_scroll=True,
            ),
            ft.ElevatedButton("Refresh", on_click=refresh_all_users_game_rooms),
            ft.Row(
                [
                    ft.TextField(
                        expand=True,
                        ref=input_ref,
                        hint_text="Message",
                        autofocus=True,
                        on_submit=on_send_clicked,
                    ),
                    ft.ElevatedButton("Send", on_click=on_send_clicked),
                ]
            ),
        ],
    )


def build_users_column():
    return ft.Column(
        expand=True,
        controls=[
            ft.Text("Users"),
            ft.ListView(
                ref=users_ref,
                expand=True,
                spacing=10,
                auto_scroll=True,
                width=500,
            ),
        ],
    )


def build_rooms_column():
    return ft.Column(
        expand=True,
        controls=[
            ft.Text("Rooms"),
            ft.ListView(
                ref=rooms_ref,
                expand=True,
                spacing=10,
                auto_scroll=True,
                width=500,
            ),
        ],
    )


def main(page):
    global client_socket

    page.title = "DashBoardAdmin.io"

    main_row = ft.Row(
        expand=True,
        controls=[
            build_users_column(),
            build_rooms_column(),
            build_chat_column(),
        ],
        spacing=10,
    )

    page.horizontally_centered = True
    page.add(main_row)

    server.server()

    client_socket = connect_to_server(
        SERVER_HOST,
        SERVER_PORT,
        on_message=on_response_received,
    )


ft.app(target=main)
