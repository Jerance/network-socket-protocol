import socket
import threading
from typing import Callable
from protocol.error_protocol import ResponseError

from protocol.protocol import parse_response, serialize_request
from protocol.protocol_commons import Request


def connect_to_server(host: str, port: int, on_message: Callable) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to server on port", port)

    # Execute infinite read in a threaded function
    # takes a callback function as argument
    thread = threading.Thread(target=socket_read, args=(client_socket, on_message))
    thread.start()

    return client_socket


def send_request(client_socket: socket.socket, request: Request) -> None:
    print(f"Sending request. request={request}")
    message = serialize_request(request)
    client_socket.send(message.encode())


def socket_read(client_socket, on_response: Callable) -> None:
    while True:
        data = client_socket.recv(1024)
        received_message = data.decode()

        try:
            response = parse_response(received_message)
            on_response(response)
        except ValueError:
            response = ResponseError("Something went wrong with the server")
            on_response(response)
