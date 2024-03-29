"""
games.py: the interface to our game data.
"""
import random

import data.db_connect as dbc

GAMES_COLLECT = 'games'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

NAME = 'name'
NUM_PLAYERS = 'numPlayers'

games = {}


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_game():
    test_game = {}
    test_game[NAME] = _get_test_name()
    test_game[NUM_PLAYERS] = 0
    return test_game


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_games() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, GAMES_COLLECT)


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(GAMES_COLLECT, {NAME: name})


def add_game(name: str, num_players: int) -> bool:
    if exists(name):
        raise ValueError(f'Duplicate game name: {name=}')
    if not name:
        raise ValueError('Game name may not be blank')
    game = {}
    game[NAME] = name
    game[NUM_PLAYERS] = num_players
    dbc.connect_db()
    _id = dbc.insert_one(GAMES_COLLECT, game)
    return _id is not None


def del_game(name: str):
    if exists(name):
        return dbc.del_one(GAMES_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def get_name(game):
    return game.get(NAME, '')


def main():
    print(get_games())


if __name__ == '__main__':
    main()
