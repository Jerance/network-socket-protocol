# method to transform message into ClientListGame
import re
from commons.models import ClientListGame


def transform_message_to_client_list_game(message: str) -> list[ClientListGame]:
    final_list: list[ClientListGame] = []
    if message == "empty":
        return final_list

    game_string_tab = message.split("/")
    for game_string in game_string_tab:
        game_tab = game_string.split(",")
        c = ClientListGame(id=int(game_tab[0]), name=game_tab[1])
        final_list.append(c)
    print(f"final : {final_list}")
    return final_list


def transform_game_list_to_string(game_list: list[ClientListGame]) -> str:
    final_str = ""
    if len(game_list) == 0:
        return "empty"
    for i in range(len(game_list)):
        final_str += (
            f"{game_list[i].id},{game_list[i].name}/"
            if (i != (len(game_list) - 1))
            else f"{game_list[i].id},{game_list[i].name}"
        )
    return final_str
