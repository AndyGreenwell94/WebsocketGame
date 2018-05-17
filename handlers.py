import tornado.websocket
import tornado.web
import uuid
import json

from game_manager import GameManager


class GameSocketHandler(tornado.websocket.WebSocketHandler):
    game_manager = GameManager()
    connections = {}

    def open(self, *args, **kwargs):
        self.guid = str(uuid.uuid4())
        self.connections[self.guid] = self
        state = self.game_manager.add_player(self.guid)
        self.send_state(state)

    def on_message(self, message):
        print(message)
        state = self.game_manager.handle_act(self.guid, message)
        self.send_state(state)

    @classmethod
    def send_state(cls, state):
        for player in state['players']:
            cls.connections[player['guid']].write_message(json.dumps(state))

    def on_close(self):
        state = self.game_manager.end_game(self.guid)
        self.send_state(state)
