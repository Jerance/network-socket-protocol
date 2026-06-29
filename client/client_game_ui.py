import socket
import pygame
import sys

from client import connect_to_server, send_request
from protocol.error_protocol import ResponseError
from protocol.protocol_commons import Response
from protocol.user_protocol import RequestUserCreate, ResponseUser, ResponseUserCreate

SERVER_HOST = "localhost"

SERVER_PORT = 2020
client_socket: socket.socket | None = None

# pygame setup
pygame.init()


def on_click_pseudo_input(pseudo: str):
    request = RequestUserCreate(name=pseudo)
    send_request(client_socket, request)


def on_user_response_received(response: ResponseUser):
    match response:
        case ResponseUserCreate():
            global is_input_show
            is_input_show = not response.status_ok
        case _:
            pass


def on_response_received(response: Response):
    match response:
        case ResponseUser():
            on_user_response_received(response)
        case _:
            ResponseError(error_message="Unknown response type")


client_socket = connect_to_server(
    SERVER_HOST,
    SERVER_PORT,
    on_message=on_response_received,
)


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

is_input_show = True

# Taille fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Création de joueur")

font = pygame.font.Font(None, 32)

input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color = color_inactive
active = False
text = ""
text_surface = font.render(text, True, color)

button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
button_color = pygame.Color("red")
button_text = font.render("Submit", True, WHITE)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if is_input_show == True and event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
            if button.collidepoint(event.pos):
                on_click_pseudo_input(text)
                text = ""
                text_surface = font.render(text, True, color)
        if is_input_show == True and event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                text_surface = font.render(text, True, color)

    screen.fill(BLACK)

    if is_input_show == True:
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, button_color, button)
        screen.blit(button_text, (button.x + 15, button.y + 15))

    pygame.display.flip()

pygame.quit()
sys.exit()
