from unittest import TestCase
import unittest
from commons.models import ClientListGame

from protocol.game_protocol import (
    ResponseGameList,
    parse_game_response,
    serialize_game_response,
)


class ProtocolTest(TestCase):

    def test_transform_game_list_to_string(self):
        response = serialize_game_response(
            ResponseGameList(
                games=[
                    ClientListGame(id=1, name="game 1"),
                    ClientListGame(id=2, name="game 2"),
                ]
            )
        )
        self.assertEqual(response, "GAME list 1,game 1/2,game 2")

    def test_transform_message_to_client_list_game(self):
        response = parse_game_response(["GAME", "list", "1,game 1/2,game 2"])
        a = ResponseGameList(
            games=[
                ClientListGame(id=1, name="game 1"),
                ClientListGame(id=2, name="game 2"),
            ]
        )

        self.assertEqual(
            response,
            a,
        )


if __name__ == "__main__":
    unittest.main()
