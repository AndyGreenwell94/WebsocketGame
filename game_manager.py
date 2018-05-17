from game_engine import Game, Player
import uuid


class GameManager(object):

    def __init__(self):
        self.players = {}
        self.connections = {}
        self.running_games = {}
        self.waiting_games = []

    def new_player(self, player_guid):
        player = Player(player_guid)
        self.players[player_guid] = player
        return player

    def add_player(self, player_guid):
        player = self.new_player(player_guid)
        if len(self.waiting_games) > 0:
            game = self.waiting_games.pop(0)
        else:
            game = Game(str(uuid.uuid4()))
            self.waiting_games.append(game)
        state = game.add_player(player)
        if len(game.players) == 2:
            self.running_games[game.guid] = game
        return state

    def handle_act(self, player_guid, action):
        player = self.players.get(player_guid)
        game = player.game
        game.act(player, action)
        return game.get_state()

    def end_game(self, player_guid):
        player = self.players[player_guid]
        state = player.game.end_game(losser=player)
        return state
