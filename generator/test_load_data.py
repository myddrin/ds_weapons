import json

from generator.load_data import load_csv
from storage.objects import Deck


def test_load_data():
    with open('../test_data/ex_base_game.json') as f:
        init_json = json.load(f)
    game = Deck.from_json_file('../test_data/ex_base_game.json')

    new_json = game.to_json()
    assert new_json == init_json


def test_load_csv():
    game = Deck.from_json_file('base_game_characters_only.json')
    load_csv(game, '../test_data/ex_weapons.csv')
    with open('../test_data/ex_base_game.json') as f:
        init_json = json.load(f)
    new_json = game.to_json()

    def _key(e):
        return e['name']

    for k, v in init_json.items():
        if isinstance(v, list):
            assert sorted(v, key=_key) == sorted(new_json[k], key=_key)
        else:
            assert v == new_json[k]
