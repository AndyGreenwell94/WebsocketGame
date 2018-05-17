from itertools import cycle
from random import randint, shuffle


class Player(object):

    ATTACK_ACTION = 'ATTACK'
    HEAL_ACTION = 'HEAL'

    KILLED_SIGNAL = 'KILLED'
    SURVIVED_SIGNAL = 'SURVIVED'
    HEALED_SIGNAL = 'HEALED'

    def __init__(self, guid):
        self.guid = guid
        self.health = 10
        self.attack_range = (1, 3)
        self.heal_range = (0, 4)
        self.game = None

    def set_game(self, game):
        self.game = game

    def act(self, action, data):
        if action == self.ATTACK_ACTION:
            return self.attack(data)
        if action == self.HEAL_ACTION:
            return self.heal(data)

    def attack(self, enemy: 'Player'):
        attack_power = randint(*self.attack_range)
        return enemy.take_damage(attack_power)

    def heal(self, *args):
        heal_power = randint(*self.heal_range)
        self.health += heal_power
        return self.HEALED_SIGNAL

    def take_damage(self, attack):
        self.health -= attack
        if self.health <= 0:
            return self.KILLED_SIGNAL
        return self.SURVIVED_SIGNAL

    def get_state(self):
        return {
            'guid': self.guid,
            'health': self.health,
        }


class Game(object):

    START_GAME = 'START_GAME'
    END_GAME = 'END_GAME'
    WAITING_FOR_PLAYERS = 'WAITING_FOR_PLAYERS'

    GAME_FULL = 'GAME_FULL'

    END_TURN = 'END_TURN'

    WRONG_PLAYER = 'WRONG_PLAYER'

    def __init__(self, guid):
        self.guid = guid
        self.players = []
        self.turn = -1
        self.current_player = None
        self.winner = None
        self.turn_generator = None
        self.state = self.WAITING_FOR_PLAYERS

    def add_player(self, player):
        if len(self.players) < 2:
            player.set_game(self)
            self.players.append(player)
        else:
            return self.GAME_FULL
        if len(self.players) == 2:
            return self.start_game()
        return self.get_state()

    def start_game(self):
        self.turn = 0
        shuffle(self.players)
        self.turn_generator = cycle(self.players)
        self.current_player = self.turn_generator.__next__()
        self.state = self.START_GAME
        return self.get_state()

    def end_turn(self):
        self.turn += 1
        self.toggle_player()
        return self.END_TURN

    def end_game(self, winner=None, looser=None):
        if winner:
            self.winner = winner
        else:
            self.winner = filter(lambda player: player != looser).__next__()
        self.state = self.END_GAME
        return self.get_state()

    def act(self, player, action):
        if self.current_player == player:
            signal = player.act(action)
            if signal == Player.KILLED_SIGNAL:
                return self.end_game(winner=self.current_player)
            return self.end_turn()
        player.take_damage(1)
        return self.WRONG_PLAYER

    def toggle_player(self):
        self.current_player = self.turn_generator.__next__()

    def get_state(self):
        return {
            'guid': self.guid,
            'status': self.state,
            'players': [player.get_state() for player in self.players],
        }
